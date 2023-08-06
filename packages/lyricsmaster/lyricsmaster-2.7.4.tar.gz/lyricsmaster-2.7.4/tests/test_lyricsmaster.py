#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `lyricsmaster` package."""

import os
import sys
import codecs

import pytest
from click.testing import CliRunner

from bs4 import BeautifulSoup, Tag

import requests

from lyricsmaster import models
from lyricsmaster import cli
from lyricsmaster import lyricsmaster
from lyricsmaster.utils import TorController, normalize

try:
    basestring  # Python 2.7 compatibility
except NameError:
    basestring = str

python_is_outdated = '2.7' in sys.version or '3.3' in sys.version
is_appveyor = 'APPVEYOR' in os.environ
is_travis = 'TRAVIS' in os.environ

user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'}
session = requests.Session()
session.headers = user_agent

@pytest.fixture(scope="module")
def songs():
    songs = [models.Song(real_singer['songs'][0]['song'], real_singer['album'], real_singer['name'],
                         real_singer['songs'][0]['lyrics']),
             models.Song(real_singer['songs'][1]['song'], real_singer['album'], real_singer['name'],
                         real_singer['songs'][1]['lyrics'])]
    return songs


real_singer = {'name': 'The Notorious B.I.G.', 'album': 'Ready to Die (1994)',
               'songs': [{'song': 'Things Done Changed', 'lyrics': 'Remember back in the days...'},
                         {'song': 'Things Done Changed', 'lyrics': 'Remember back in the days...'}]
               }
fake_singer = {'name': 'Fake Rapper', 'album': "In my mom's basement", 'song': 'I fap',
               'lyrics': 'Everyday I fap furiously...'}

providers = [ lyricsmaster.Genius(), lyricsmaster.LyricWiki()]

provider_strings = {
    'LyricWiki': {'artist_name': 'The_Notorious_B.I.G.',
                  'artist_url': 'http://lyrics.wikia.com/wiki/The_Notorious_B.I.G.',
                  'song_url': 'http://lyrics.wikia.com/wiki/The_Notorious_B.I.G.:Things_Done_Changed',
                  'fake_url': 'http://lyrics.wikia.com/wiki/Things_Done_Changed:Things_Done_Changed_fake_url'},
    'AzLyrics': {'artist_name': 'notorious',
                 'artist_url': 'https://www.azlyrics.com/n/notorious.html',
                 'song_url': 'https://www.azlyrics.com/lyrics/notoriousbig/thingsdonechanged.html',
                 'fake_url': 'https://www.azlyrics.com/lyrics/notoriousbig/thingsdonechanged_fake.html'},
    'Genius': {'artist_name': 'The-notorious-big',
                 'artist_url': 'https://genius.com/artists/The-notorious-big',
                 'song_url': 'https://genius.com/The-notorious-big-things-done-changed-lyrics',
                 'fake_url': 'https://genius.com/The-notorious-big-things-done-changed-lyrics_fake'}
}

class TestSongs:
    """Tests for Song Class."""
    song = songs()[0]

    def test_song(self):
        assert self.song.__repr__() == 'lyricsmaster.models.Song({0}, {1}, {2})'.format(real_singer['songs'][0]['song'],
                                                                                        real_singer['album'],
                                                                                        real_singer['name'])

    def test_song_save(self):
        self.song.save()
        path = os.path.join(os.path.expanduser("~"), 'Documents', 'LyricsMaster', normalize(real_singer['name']),
                            normalize(real_singer['album']), 'Things-Done-Changed.txt')
        assert os.path.exists(path)
        folder = os.path.join(os.path.expanduser("~"), 'Documents', 'test_lyricsmaster_save')
        self.song.save(folder)
        path = os.path.join(folder, 'LyricsMaster', normalize(real_singer['name']), normalize(real_singer['album']),
                            'Things-Done-Changed.txt')
        assert os.path.exists(path)
        with codecs.open(path, 'r', encoding='utf-8') as file:
            assert self.song.lyrics == file.readlines()[0]


class TestAlbums:
    """Tests for Album Class."""

    songs = songs()
    album = models.Album(real_singer['album'], real_singer['name'], songs)

    def test_album(self):
        assert self.album.__idx__ == 0
        assert self.album.title == real_singer['album']
        assert self.album.author == real_singer['name']
        assert self.album.__repr__() == 'lyricsmaster.models.Album({0}, {1})'.format(real_singer['album'],
                                                                                     real_singer['name'])

    def test_album_isiter(self):
        assert len(self.album) == 2
        assert [elmt for elmt in self.album] == self.songs
        for x, y in zip(reversed(self.album), reversed(self.album.songs)):
            assert x == y

    def test_album_save(self):
        self.album.save()
        for song in self.album.songs:
            author = normalize(song.author)
            album = normalize(song.album)
            title = normalize(song.title)
            path = os.path.join(os.path.expanduser("~"), 'Documents', 'LyricsMaster', author, album, title + '.txt')
            assert os.path.exists(path)
            with codecs.open(path, 'r', encoding='utf-8') as file:
                assert song.lyrics == '\n'.join(file.readlines())


class TestDiscography:
    """Tests for Discography Class."""

    albums = [models.Album(real_singer['album'], real_singer['name'], songs()),
              models.Album(fake_singer['album'], fake_singer['name'], songs())]
    discography = models.Discography(real_singer['name'], albums)

    def test_discography(self):
        assert self.discography.__repr__() == 'lyricsmaster.models.Discography({0})'.format(real_singer['name'])

    def test_discography_isiter(self):
        assert self.discography.__idx__ == 0
        assert len(self.discography) == 2
        assert [elmt for elmt in self.discography] == self.albums
        for x, y in zip(reversed(self.discography), reversed(self.discography.albums)):
            assert x == y

    def test_discography_save(self):
        self.discography.save()
        for album in self.albums:
            for song in album.songs:
                author = normalize(song.author)
                album = normalize(song.album)
                title = normalize(song.title)
                path = os.path.join(os.path.expanduser("~"), 'Documents', 'LyricsMaster', author, album, title + '.txt')
                assert os.path.exists(path)
                with codecs.open(path, 'r', encoding='utf-8') as file:
                    assert song.lyrics == '\n'.join(file.readlines())


class TestLyricsProviders:
    """Tests for LyricWiki Class."""

    @pytest.mark.skipif(is_appveyor and '3.3' in sys.version,
                        reason="[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:548) on Appveyor 3.3.")
    @pytest.mark.parametrize('provider', providers)
    def test_get_page(self, provider):
        url = 'http://non-existent-url.com'
        request = provider.get_page(url)
        assert request is None
        request = provider.get_page('http://www.google.com')
        assert request.status == 200

    @pytest.mark.parametrize('provider', providers)
    def test_clean_string(self, provider):
        assert provider._clean_string(real_singer['name']) == provider_strings[provider.name]['artist_name']

    @pytest.mark.parametrize('provider', providers)
    def test_has_artist(self, provider):
        clean = provider._clean_string
        url = provider._make_artist_url(clean(real_singer['name']))
        page = BeautifulSoup(session.get(url).text, 'lxml')
        assert provider._has_artist(page)
        url = provider._make_artist_url(clean(fake_singer['name']))
        page = BeautifulSoup(session.get(url).text, 'lxml')
        assert not provider._has_artist(page)

    @pytest.mark.parametrize('provider', providers)
    def test_make_artist_url(self, provider):
        clean = provider._clean_string
        assert provider._make_artist_url(
            clean(real_singer['name'])) == provider_strings[provider.name]['artist_url']

    @pytest.mark.parametrize('provider', providers)
    def test_get_artist_page(self, provider):
        page = provider.get_artist_page(real_singer['name'])
        assert '<!doctype html>' in str(page).lower()
        page = provider.get_artist_page(fake_singer['name'])
        assert page is None

    @pytest.mark.parametrize('provider', providers)
    def test_get_album_page(self, provider):
        if provider.name in ('AzLyrics', 'Genius'):
            return
        else:
            page = provider.get_album_page(real_singer['name'], fake_singer['album'])
            assert page is None
            page = provider.get_album_page(fake_singer['name'], fake_singer['album'])
            assert page is None
            page = provider.get_album_page(real_singer['name'], real_singer['album'])
            assert '<!doctype html>' in str(page).lower()

    @pytest.mark.parametrize('provider', providers)
    def test_has_lyrics(self, provider):
        url = provider_strings[provider.name]['song_url']
        page = BeautifulSoup(session.get(url).text, 'lxml')
        assert provider._has_lyrics(page)
        url = provider_strings[provider.name]['fake_url']
        page = BeautifulSoup(session.get(url).text, 'lxml')
        assert not provider._has_lyrics(page)

    @pytest.mark.parametrize('provider', providers)
    def test_get_lyrics_page(self, provider):
        page = provider.get_lyrics_page(provider_strings[provider.name]['song_url'])
        assert '<!doctype html>' in str(page).lower()
        page = provider.get_lyrics_page(provider_strings[provider.name]['fake_url'])
        assert page is None

    @pytest.mark.parametrize('provider', providers)
    def test_get_albums(self, provider):
        url = provider_strings[provider.name]['artist_url']
        page = session.get(url).text
        albums = provider.get_albums(page)
        for album in albums:
            assert isinstance(album, Tag)

    @pytest.mark.parametrize('provider', providers)
    def test_get_album_title(self, provider):
        url = provider_strings[provider.name]['artist_url']
        page = session.get(url).text
        album = provider.get_albums(page)[0]
        album_title = provider.get_album_title(album)
        assert album_title in (real_singer['album'], 'Demo Tape') # 'Demo Tape' for Genius

    @pytest.mark.parametrize('provider', providers)
    def test_extract_lyrics(self, provider):
        page = provider.get_lyrics_page(provider_strings[provider.name]['song_url'])
        lyrics = provider.extract_lyrics(page)
        assert isinstance(lyrics, basestring)
        assert 'Remember back in the days'.lower() in lyrics.lower()
        assert "Don't ask me why I'm motherfuckin".lower() in lyrics.lower()

    @pytest.mark.parametrize('provider', providers)
    def test_get_songs(self, provider):
        author_page = provider.get_artist_page(real_singer['name'])
        album = provider.get_albums(author_page)[0]
        song_links = provider.get_songs(album)
        for link in song_links:
            assert isinstance(link, Tag)

    @pytest.mark.parametrize('provider', providers)
    def test_create_song(self, provider):
        author_page = provider.get_artist_page(real_singer['name'])
        album = provider.get_albums(author_page)[0]
        song_links = provider.get_songs(album)
        song_links[-1].attrs['href'] = provider_strings[provider.name]['fake_url']#.replace(provider.base_url, '')
        fail_song = provider.create_song(song_links[-1], real_singer['name'], real_singer['album'])
        assert fail_song is None
        good_song = provider.create_song(song_links[1], real_singer['name'], real_singer['album'])
        assert isinstance(good_song, models.Song)
        assert isinstance(good_song.title, basestring)
        assert good_song.album == real_singer['album']
        assert good_song.author == real_singer['name']
        assert isinstance(good_song.lyrics, basestring)
        # Tests existing song with empty lyrics
        if provider.name == 'LyricWiki':
            tag = '<a href="http://lyrics.wikia.com/wiki/Reggie_Watts:Feel_The_Same" class="new" title="Reggie Watts:Feel The Same (page does not exist)">Feel the Same</a>'
            page = BeautifulSoup(tag, 'lxml')
            page.attrs['title'] = "Reggie Watts:Feel The Same (page does not exist)"
            page.attrs['href'] = "http://lyrics.wikia.com/wiki/Reggie_Watts:Feel_The_Same"
            non_existent_song = provider.create_song(page, real_singer['name'], real_singer['album'])
            assert non_existent_song == None

    @pytest.mark.parametrize('provider', providers)
    def test_get_lyrics(self, provider):
        discography = provider.get_lyrics('Reggie Watts')  # put another realsinger who has not so many songs to speed up testing.
        assert isinstance(discography, models.Discography)
        discography = provider.get_lyrics(fake_singer['name'])
        assert discography is None
        discography = provider.get_lyrics('Reggie Watts', 'Why $#!+ So Crazy?')
        assert isinstance(discography, models.Discography)
        discography = provider.get_lyrics('Reggie Watts', 'Why $#!+ So Crazy?', 'Fuck Shit Stack')
        assert isinstance(discography, models.Discography)


class TestCli:
    """Tests for Command Line Interface."""

    @pytest.mark.skipif(is_appveyor and python_is_outdated, reason="Tor error on 2.7 and 3.3.")
    def test_command_line_interface(self):
        artist = 'Reggie Watts'
        runner = CliRunner()
        result = runner.invoke(cli.main, [artist, '-a', 'Why $#!+ So Crazy?', '-s', 'Fuck Shit Stack'])
        assert result.exit_code == 0
        assert 'Why $#!+ So Crazy?' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert 'Show this message and exit.' in help_result.output
        # Removed test with optional arguments. Need to check click docs for passing optional args to Clirunner.
        result_tor = runner.invoke(cli.main, [artist, '--tor', '127.0.0.1'])
        assert result_tor.exit_code == 0
        assert 'Downloading Simplified' in result_tor.output

    @pytest.mark.skipif(is_travis or (is_appveyor and python_is_outdated), reason="Skip this Tor test when in CI")
    def test_command_line_interface_tor(self):
        artist = 'Reggie Watts'
        runner = CliRunner()
        result_tor1 = runner.invoke(cli.main, [artist, '--tor', '127.0.0.1', '--controlport', '9051', '--password', 'password'])
        assert result_tor1.exit_code == 0
        assert 'Downloading Simplified' in result_tor1.output


# If tests involving Tor are run first, the following tests fail with error: 'an integer is required (got type object)'
class TestTor:
    """Tests for Tor functionality."""
    tor_basic = TorController()
    if is_travis or (is_appveyor and python_is_outdated):
        tor_advanced = TorController(controlport='/var/run/tor/control', password='password')
    else:
        tor_advanced = TorController(controlport=9051, password='password')

    provider = lyricsmaster.LyricWiki(tor_basic)
    provider2 = lyricsmaster.LyricWiki(tor_advanced)

    @pytest.mark.skipif(is_appveyor and python_is_outdated, reason="Tor error on 2.7 and 3.3.")
    def test_anonymisation(self):
        anonymous_ip = self.provider.get_page("http://httpbin.org/ip").data
        real_ip = session.get("http://httpbin.org/ip").text
        assert real_ip != anonymous_ip

    # this function is tested out in travis using a unix path as a control port instead of port 9051.
    # for now gets permission denied on '/var/run/tor/control' in Travis CI
    @pytest.mark.skipif(is_travis or (is_appveyor and python_is_outdated), reason="Skip this Tor test when in CI")
    def test_renew_tor_session(self):
        anonymous_ip = self.provider2.get_page("http://httpbin.org/ip").data
        real_ip = session.get("http://httpbin.org/ip").text
        assert real_ip != anonymous_ip
        new_tor_circuit = self.provider2.tor_controller.renew_tor_circuit()
        anonymous_ip2 = self.provider2.get_page("http://httpbin.org/ip").data
        real_ip2 = session.get("http://httpbin.org/ip").text
        assert real_ip2 != anonymous_ip2
        assert new_tor_circuit == True

    @pytest.mark.skipif(is_appveyor and python_is_outdated, reason="Tor error on 2.7 and 3.3.")
    def test_get_lyrics_tor_basic(self):
        discography = self.provider.get_lyrics(
            'Reggie Watts')  # put another realsinger who has not so many songs to speed up testing.
        assert isinstance(discography, models.Discography)

    @pytest.mark.skipif(is_travis or (is_appveyor and python_is_outdated), reason="Skip this Tor test when in CI")
    def test_get_lyrics_tor_advanced(self):
        discography = self.provider2.get_lyrics(
            'Reggie Watts')  # put another realsinger who has not so many songs to speed up testing.
        assert isinstance(discography, models.Discography)



