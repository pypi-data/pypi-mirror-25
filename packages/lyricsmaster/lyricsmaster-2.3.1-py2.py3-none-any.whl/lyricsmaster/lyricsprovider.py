# -*- coding: utf-8 -*-

"""Lyrics Providers."""
from .lyricsmaster import Song, Album, Discography

import requests
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

from stem import Signal
from stem.control import Controller


class LyricsProvider:
    """
    This is the base class for all Lyrics Providers. If you wish to sublass this class, you must implement all
    the methods defined in this class to be compatible with the LyricsMaster API.
    Requests to fetch songs are executed asynchronously for better performance.
    TOR anonymisation is provided if tor is installed on the system and a TorController is passed at instance creation.
    If 'controlport' is None, all tor connexions will use the same tor circuit.
    If 'controlport' is set, a new tor circuit will be created for each album downloaded and asynchronous requests
    are disabled for compatibility.

    :param tor: boolean.
        Whether to activate TOR proxying.
    """
    def __init__(self, tor_controller=None):
        self.tor_controller = tor_controller
        if not self.tor_controller:
            self.session = requests.session()
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
            req = self.session.get(url)
        except:
            req = None
            print('Unable to download url ' + url)
        return req

    def get_lyrics(self, author):
        """
        Must be implemented by children classes conforming to the LyricsMaster API.

        :param author:
        """
        pass

    def get_artist_page(self, author):
        """
        Must be implemented by children classes conforming to the LyricsMaster API.

        :param author:
        """
        pass

    def get_album_page(self, author, album):
        """
        Must be implemented by children classes conforming to the LyricsMaster API.

        :param author:
        :param album:
        """
        pass

    def get_lyrics_page(self, url):
        """
        Must be implemented by children classes conforming to the LyricsMaster API.

        :param url:
        """
        pass

    def extract_lyrics(self, song):
        """
        Must be implemented by children classes conforming to the LyricsMaster API.

        :param song:
        """
        pass


class LyricWiki(LyricsProvider):
    """
    Class interfacing with http://lyrics.wikia.com
    This class is used to retrieve lyrics from LyricWiki.

    """
    base_url = 'http://lyrics.wikia.com'

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

    def get_artist_page(self, author):
        """
        Fetches the web page for the supplied artist.

        :param author: string.
            Artist name.
        :return: BeautifulSoup Object.
            Artist page.
        """
        author = self.clean_string(author)
        url = self.base_url + '/wiki/' + author
        artist_page = BeautifulSoup(self.get_page(url).text, 'lxml')
        if artist_page.find("div", {'class': 'noarticletext'}):
            return None
        return artist_page

    def get_album_page(self, author, album):
        """
        Fetches the album page for the supplied artist and album.

        :param author: string.
            Artist name.
        :param album: string.
            Album title.
        :return: BeautifulSoup Object or None.
            Album page.
        """
        author = self.clean_string(author)
        album = self.clean_string(album)
        url = self.base_url + '/wiki/' + author + ':' + album
        album_page = BeautifulSoup(self.get_page(url).text, 'lxml')
        if album_page.find("div", {'class': 'noarticletext'}):
            return None
        return album_page

    def get_lyrics_page(self, url):
        """
        Fetches the web page containing the lyrics at the supplied url.

        :param url: string.
            Lyrics url.
        :return: BeautifulSoup Object or None.
            Lyrics page.
        """
        lyrics_page = BeautifulSoup(self.get_page(url).text, 'lxml')
        if lyrics_page.find("div", {'class': 'noarticletext'}):
            return None
        return lyrics_page

    def get_songs(self, album):
        """
        Fetches the links to the songs of the supplied album.

        :param album: BeautifulSoup Object.
        :return: List of BeautifulSoup Tag Objects.
        """
        parent_node = album.parent
        while parent_node.name != 'ol':
            parent_node = parent_node.next_sibling
        song_links = parent_node.find_all('li')
        return song_links

    def extract_lyrics(self, song):
        """
        Extracts the lyrics from the lyrics page of the supplied song.

        :param song: BeautifulSoup Object.
            Lyrics page.
        :return: string.
            Formatted lyrics.
        """
        lyric_box = song.find("div", {'class': 'lyricbox'})
        lyrics = '\n'.join(lyric_box.strings)
        return lyrics

    def create_song(self, link, author, album_title):
        """
        Creates a Song object

        :param link: BeautifulSoup Link Object.
        :param author: string.
        :param album_title: string.
        :return: lyricsmaster.Song Object or None.
        """
        link = link.find('a')
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

    def get_lyrics(self, author):
        """
        This is the main method of this class.
        Connects to LyricWiki and downloads lyrics for all the albums of the supplied artist.
        Returns a Discography Object or None if the artist was not found on LyricWiki.

        :param author: string
            Artist name.
        :return: lyricsmaster.Discography Object or None.
        """
        artist_page = self.get_artist_page(author)
        if not artist_page:
            return None
        albums = [tag for tag in
                  artist_page.find_all("span", {'class': 'mw-headline'}) if
                  tag.attrs['id'] not in (
                      'Additional_information', 'External_links')]
        album_objects = []
        if self.__async_enabled__:  #
            # cycle circuits
            gevent.monkey.patch_socket()
        for elmt in albums:
            album_title = elmt.text
            song_links = self.get_songs(elmt)
            print('Downloading {0}'.format(elmt.text))
            if self.tor_controller and self.tor_controller.controlport:
                self.tor_controller.renew_tor_circuit()
                self.session = self.tor_controller.get_tor_session()
                songs = [self.create_song(link, author, album_title) for link in
                         song_links]
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


if __name__ == "__main__":
    pass
