# -*- coding: utf-8 -*-

"""Main module.

This module defines the Api interface for the various Lyrics providers.
All lyrics providers inherit from the base class LyricsProvider.

"""

from abc import ABCMeta, abstractmethod

from .models import Song, Album, Discography

import re
import urllib3
from bs4 import BeautifulSoup

import gevent.monkey
from gevent.pool import Pool

import socket

try:
    from importlib import reload
except ImportError:
    try:
        from imp import reload
    except:
        pass


class LyricsProvider:
    """
    This is the base class for all Lyrics Providers. If you wish to subclass this class, you must implement all
    the methods defined in this class to be compatible with the LyricsMaster API.
    Requests to fetch songs are executed asynchronously for better performance.
    Tor anonymisation is provided if tor is installed on the system and a TorController is passed at instance creation.

    :param tor_controller: TorController Object.

    """
    __metaclass__ = ABCMeta

    def __init__(self, tor_controller=None):
        self.tor_controller = tor_controller
        if not self.tor_controller:
            self.session = urllib3.PoolManager(maxsize=10)
            # self.session = requests.session()
            print(
                'Asynchronous requests enabled. The connexion is not anonymous.')
        else:
            self.session = self.tor_controller.get_tor_session()
            print('Anonymous requests enabled.')
            if not self.tor_controller.controlport:
                print(
                    'Asynchronous requests enabled but the tor circuit will not change for each album.')
            else:
                print(
                    'Asynchronous requests disabled to allow the creation of new tor circuits for each album')

    def __repr__(self):
        return '{0}.{1}({2})'.format(__name__, self.__class__.__name__, self.tor_controller.__repr__())

    @property
    def __async_enabled__(self):
        return not self.tor_controller or (self.tor_controller and not self.tor_controller.controlport)

    def get_page(self, url):
        """
        Fetches the supplied url and returns a request object.

        :param url: string.
        :return: requests.request Object.
        """
        try:
            req = self.session.request('GET', url)
        except Exception as e:
            print(e)
            req = None
            print('Unable to download url ' + url)
        return req

    def get_lyrics(self, author):
        """
        This is the main method of this class.
        Connects to LyricWiki and downloads lyrics for all the albums of the supplied artist.
        Returns a Discography Object or None if the artist was not found on LyricWiki.

        :param author: string
            Artist name.
        :return: models.Discography object or None.
        """
        raw_html = self.get_artist_page(author)

        if not raw_html:
            return None
        albums = self.get_albums(raw_html)
        album_objects = []
        if self.__async_enabled__:
            # cycle circuits
            gevent.monkey.patch_socket()
        for elmt in albums:
            album_title = self.get_album_title(elmt)
            song_links = self.get_songs(elmt)
            print('Downloading {0}'.format(album_title))
            if self.tor_controller and self.tor_controller.controlport:
                self.tor_controller.renew_tor_circuit()
                self.session = self.tor_controller.get_tor_session()
                songs = [self.create_song(link, author, album_title) for link in song_links]
            else:
                pool = Pool(25)  # Sets the worker pool for async requests
                results = [
                    pool.spawn(self.create_song, *(link, author, album_title))
                    for link in song_links]
                pool.join()  # Gathers results from the pool
                songs = [song.value for song in results]
            album = Album(album_title, author, songs)
            album_objects.append(album)
        if self.__async_enabled__:
            reload(socket)
        discography = Discography(author, album_objects)
        return discography

    @abstractmethod
    def get_artist_page(self, author):
        """
        Must be implemented by children classes conforming to the LyricsMaster API.

        Fetches the web page for the supplied artist.

        :param author: string.
            Artist name.
        :return: string.
            Artist's raw html page.
        """
        pass

    @abstractmethod
    def get_lyrics_page(self, url):
        """
        Must be implemented by children classes conforming to the LyricsMaster API.

        Fetches the web page containing the lyrics at the supplied url.

        :param url: string.
            Lyrics url.
        :return: string or None.
            Lyrics's raw html page.
        """
        pass

    @abstractmethod
    def get_albums(self, raw_artist_page):
        """
        Fetches the albums section in the supplied html page.

        :param raw_artist_page: Artist's raw html page.
        :return: list.
            List of BeautifulSoup objects.
        """
        pass

    @abstractmethod
    def get_album_title(self, tag):
        """
        Must be implemented by children classes conforming to the LyricsMaster API.

        Extracts the Album title from the tag

        :param tag: BeautifulSoup object.
        :return: string.
            Album title.
        """
        pass

    @abstractmethod
    def get_songs(self, album):
        """
        Must be implemented by children classes conforming to the LyricsMaster API.

        Fetches the links to the songs of the supplied album.

        :param album: BeautifulSoup object.
        :return: List of BeautifulSoup Link objects.
        """
        pass

    @abstractmethod
    def create_song(self, link, author, album_title):
        """
        Must be implemented by children classes conforming to the LyricsMaster API.

        Creates a Song object.

        :param link: BeautifulSoup Link object.
        :param author: string.
        :param album_title: string.
        :return: models.Song object or None.
        """
        pass

    @abstractmethod
    def extract_lyrics(self, song):
        """
        Must be implemented by children classes conforming to the LyricsMaster API.

        Extracts the lyrics from the lyrics page of the supplied song.

        :param song: string.
            Lyrics's raw html page.
        :return: string.
            Formatted lyrics.
        """
        pass


class LyricWiki(LyricsProvider):
    """
    Class interfacing with http://lyrics.wikia.com .
    This class is used to retrieve lyrics from LyricWiki.

    """
    base_url = 'http://lyrics.wikia.com'

    def get_artist_page(self, author):
        """
        Fetches the web page for the supplied artist.

        :param author: string.
            Artist name.
        :return: string or None.
            Artist's raw html page. None if the artist page was not found.
        """
        author = self.clean_string(author)
        url = self.base_url + '/wiki/' + author
        raw_html = self.get_page(url).data
        artist_page = BeautifulSoup(raw_html, 'lxml')
        if artist_page.find("div", {'class': 'noarticletext'}):
            return None
        return raw_html

    def get_album_page(self, author, album):
        """
        Fetches the album page for the supplied artist and album.

        :param author: string.
            Artist name.
        :param album: string.
            Album title.
        :return: string or None.
            Album's raw html page. None if the album page was not found.
        """
        author = self.clean_string(author)
        album = self.clean_string(album)
        url = self.base_url + '/wiki/' + author + ':' + album
        raw_html = self.get_page(url).data
        album_page = BeautifulSoup(raw_html, 'lxml')
        if album_page.find("div", {'class': 'noarticletext'}):
            return None
        return raw_html

    def get_lyrics_page(self, url):
        """
        Fetches the web page containing the lyrics at the supplied url.

        :param url: string.
            Lyrics url.
        :return: string or None.
            Lyrics's raw html page. None if the lyrics page was not found.
        """
        raw_html = self.get_page(url).data
        lyrics_page = BeautifulSoup(raw_html, 'lxml')
        if lyrics_page.find("div", {'class': 'noarticletext'}):
            return None
        return raw_html

    def get_albums(self, raw_artist_page):
        """
        Fetches the albums section in the supplied html page.

        :param raw_artist_page: Artist's raw html page.
        :return: list.
            List of BeautifulSoup objects.
        """
        artist_page = BeautifulSoup(raw_artist_page, 'lxml')
        albums = [tag for tag in artist_page.find_all("span", {'class': 'mw-headline'}) if
                  tag.attrs['id'] not in ('Additional_information', 'External_links')]
        return albums

    def get_album_title(self, tag):
        """
        Extracts the Album title from the tag

        :param tag: BeautifulSoup object.
        :return: string.
            Album title.
        """
        album_title = tag.text
        return album_title

    def get_songs(self, album):
        """
        Fetches the links to the songs of the supplied album.

        :param album: BeautifulSoup object.
        :return: List of BeautifulSoup Link objects.
        """
        parent_node = album.parent
        while parent_node.name != 'ol':
            parent_node = parent_node.next_sibling
        song_links = [elmt.find('a') for elmt in parent_node.find_all('li')]
        return song_links

    def create_song(self, link, author, album_title):
        """
        Creates a Song object.

        :param link: BeautifulSoup Link object.
        :param author: string.
        :param album_title: string.
        :return: models.Song object or None.
        """
        song_title = link.attrs['title']
        song_title = song_title[song_title.index(':') + 1:]
        if '(page does not exist' in song_title:
            return None
        lyrics_page = self.get_lyrics_page(self.base_url + link.attrs['href'])
        if not lyrics_page:
            return None
        lyrics = self.extract_lyrics(lyrics_page)
        song = Song(song_title, album_title, author, lyrics)
        return song

    def extract_lyrics(self, song):
        """
        Extracts the lyrics from the lyrics page of the supplied song.

        :param song: string.
            Lyrics's raw html page.
        :return: string.
            Formatted lyrics.
        """
        lyrics_page = BeautifulSoup(song, 'lxml')
        lyric_box = lyrics_page.find("div", {'class': 'lyricbox'})
        lyrics = '\n'.join(lyric_box.strings)
        return lyrics

    def clean_string(self, text):
        """
        Cleans the supplied string and formats it to use in a url.

        :param text: string.
            Text to be cleaned.
        :return: string.
            Cleaned text.
        """
        for elmt in [('#', 'Number_'), ('[', '('), (']', ')'), ('{', '('), ('}', ')'), (' ', '_')]:
            text = text.replace(*elmt)
        return text


class AzLyrics(LyricsProvider):
    base_url = 'https://www.azlyrics.com'

    def get_artist_page(self, author):
        """
        Fetches the web page for the supplied artist.

        :param author: string.
            Artist name.
        :return: string or None.
            Artist's raw html page. None if the artist page was not found.
        """
        author = self.clean_string(author)
        if author[0].isalpha():
            prefix = author[0]
        else:
            prefix = '19'
        url = self.base_url + '/{0}/{1}.html'.format(prefix, author)
        raw_html = self.get_page(url).data
        artist_page = BeautifulSoup(raw_html, 'lxml')
        if not artist_page.find("div", {'id': 'listAlbum'}):
            return None
        return raw_html

    def get_lyrics_page(self, url):
        """
        Fetches the web page containing the lyrics at the supplied url.

        :param url: string.
            Lyrics url.
        :return: string or None.
            Lyrics's raw html page. None if the lyrics page was not found.
        """
        raw_html = self.get_page(url).data
        lyrics_page = BeautifulSoup(raw_html, 'lxml')
        if not lyrics_page.find("div", {'class': 'lyricsh'}):
            return None
        return raw_html

    def get_albums(self, raw_artist_page):
        """
        Fetches the albums section in the supplied html page.

        :param raw_artist_page: Artist's raw html page.
        :return: list.
            List of BeautifulSoup objects.
        """
        artist_page = BeautifulSoup(raw_artist_page, 'lxml')
        albums = [tag for tag in artist_page.find_all("div", {'id': 'listAlbum'})]
        return albums

    def get_album_title(self, tag):
        """
        Extracts the Album title from the tag

        :param tag: BeautifulSoup object.
        :return: string.
            Album title.
        """
        album_title = tag.find("div", {'class': 'album'}).text
        album_title = re.findall(r'"([^"]*)"', album_title)[0]
        return album_title

    def get_songs(self, album):
        """
        Fetches the links to the songs of the supplied album.

        :param album: BeautifulSoup object.
        :return: List of BeautifulSoup Link objects.
        """
        song_links = album.find_all('a')
        song_links = [song for song in song_links if 'href' in song.attrs]
        return song_links

    def create_song(self, link, author, album_title):
        """
        Creates a Song object.

        :param link: BeautifulSoup Link object.
        :param author: string.
        :param album_title: string.
        :return: models.Song object or None.
        """
        song_title = link.text
        lyrics_page = self.get_lyrics_page(self.base_url + link.attrs['href'].replace('..', ''))
        if not lyrics_page:
            return None
        lyrics = self.extract_lyrics(lyrics_page)
        song = Song(song_title, album_title, author, lyrics)
        return song

    def extract_lyrics(self, song):
        """
        Extracts the lyrics from the lyrics page of the supplied song.

        :param song: string.
            Lyrics's raw html page.
        :return: string.
            Formatted lyrics.
        """
        lyrics_page = BeautifulSoup(song, 'lxml')
        lyric_box = lyrics_page.find("div", {"class": None, "id": None})
        lyrics = ''.join(lyric_box.strings)
        return lyrics

    def clean_string(self, text):
        """
        Cleans the supplied string and formats it to use in a url.

        :param text: string.
            Text to be cleaned.
        :return: string.
            Cleaned text.
        """
        text = "".join([c if c.isalnum() else "" for c in text])
        return text.lower()



if __name__ == "__main__":
    pass
