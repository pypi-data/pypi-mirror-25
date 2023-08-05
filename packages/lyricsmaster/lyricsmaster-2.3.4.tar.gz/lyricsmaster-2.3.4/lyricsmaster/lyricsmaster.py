# -*- coding: utf-8 -*-

"""Main module."""

import os
from codecs import open
from .utils import set_save_folder, normalize


class Song:
    """
    Song class.

    :param title string:
        Song title.
    :param album string:
        Album title.
    :param author string:
        Author name.
    :param lyrics string:
        Lyrics of the song.
    """
    __slots__ = ('title', 'album', 'author', 'lyrics')

    def __init__(self, title, album, author, lyrics=None):
        self.title = title
        self.album = album
        self.author = author
        self.lyrics = lyrics

    def __repr__(self):
        return self.__class__.__name__ + " Object: " + self.title

    def save(self, folder=None):
        """
        Saves the lyrics of the song in the supplied folder.
        The lyrics of a song are saved in folder/author/album/song_title.txt

        :param folder string:
            path to save folder.
        """
        folder = set_save_folder(folder)
        if self.lyrics:
            author = normalize(self.author)
            album = normalize(self.album)
            save_path = os.path.join(folder, author, album)
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            file_name = normalize(self.title)
            with open(os.path.join(save_path, file_name + ".txt"), "w", encoding="utf-8") as file:
                file.write(self.lyrics)


class Album:
    """
    Album Class.
    The Album class follows the Iterable protocol and can be iterated over the songs.

    :param title string:
        Album title.
    :param author string:
        Artist name.
    :param songs string:
        List of Songs objects.
    """
    __slots__ = ('__idx__', 'title', 'author', 'songs')

    def __init__(self, title, author, songs):
        self.__idx__ = 0
        self.title = title
        self.author = author
        self.songs = songs

    def __repr__(self):
        return self.__class__.__name__ + " Object: " + self.title

    def __len__(self):
        return len(self.songs)

    def __iter__(self):
        return self

    def __next__(self):
        self.__idx__ += 1
        try:
            return self.songs[self.__idx__ - 1]
        except IndexError:
            self.__idx__ = 0
            raise StopIteration

    def __reversed__(self):
        return reversed(self.songs)

    next = __next__

    def save(self, folder=None):
        """
        Saves the album to disc in the supplied folder.

        :param folder string:
            path to save folder.
        """
        for song in self.songs:
            if song:
                song.save(folder)


class Discography:
    """
    Discography Class.
    The Discography class follows the Iterable protocol and can be iterated over the albums.

    :param author string:
        Artist name.
    :param albums list:
        List of Album objects.
    """
    __slots__ = ('__idx__', 'author', 'albums')

    def __init__(self, author, albums):
        self.__idx__ = 0
        self.author = author
        self.albums = albums

    def __repr__(self):
        return self.__class__.__name__ + " Object: " + self.author

    def __len__(self):
        return len(self.albums)

    def __iter__(self):
        return self

    def __next__(self):
        self.__idx__ += 1
        try:
            return self.albums[self.__idx__ - 1]
        except IndexError:
            self.__idx__ = 0
            raise StopIteration

    def __reversed__(self):
        return reversed(self.albums)

    next = __next__

    def save(self, folder=None):
        """
        Saves Discography to disc in the supplied folder.

        :param folder string:
            Path to save folder.
        """
        for album in self.albums:
            album.save(folder)
