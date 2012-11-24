import re
from ScriptingBridge import SBApplication

__app__ = SBApplication.applicationWithBundleIdentifier_("com.apple.iTunes")
whitespace = re.compile(r'\s+')

def listify(generator):
    def patched(*args, **kw):
        return list(generator(*args, **kw))
    return patched

def arrayIterator(elementArray):
    count = elementArray.count()
    for i in range(count):
        yield elementArray.objectAtIndex_(i)

arrayLister = listify(arrayIterator)


class ITunes(object):
    def __init__(self, sb_app):
        self.__sb__ = sb_app
        self.source = arrayIterator(self.__sb__.sources()).next()

    @listify
    def playlists(self, smart=None, basic=None):
        for p in arrayIterator(self.source.userPlaylists()):
            if smart is None or p.smart() == smart:
                playlist_is_basic = p.specialKind() == 1800302446
                if basic is None or basic == playlist_is_basic:
                    yield Playlist(p)

    @property
    def library(self):
        sb_playlist = arrayIterator(self.source.libraryPlaylists()).next()
        return Playlist(sb_playlist)

    def create_playlist(self, name):
        sb_playlist = __app__.classForScriptingClass_("playlist").alloc().initWithProperties_(dict(name=name))
        self.source.playlists().addObject_(sb_playlist)
        return Playlist(sb_playlist)


class Playlist(object):
    def __init__(self, sb_playlist):
        self.__sb__ = sb_playlist

    def add_track(self, track):
        assert isinstance(track, Track)
        track.duplicateTo_(self.__sb__)

    @property
    def tracks(self):
        return [Track(sb_track) for sb_track in arrayIterator(self.__sb__.tracks())]

    def __str__(self):
        return self.__sb__.name()


class Track(object):
    def __init__(self, sb_track):
        self.__sb__ = sb_track

    @property
    def artist(self):
        return self.__sb__.artist()

    @property
    def album(self):
        return self.__sb__.album()

    @property
    def name(self):
        return self.__sb__.name()

    @property
    def plays(self):
        return self.__sb__.playedCount()

    @property
    def rating(self):
        return self.__sb__.rating()

    @property
    def comment(self):
        return whitespace.sub(' ', self.__sb__.comment())

    @property
    def added_ticks(self):
        return int(self.__sb__.dateAdded().timeIntervalSince1970())

    def set(self, key, value):
        # assert key in ['plays', 'rating', 'comment']
        if key == 'plays':
            self.__sb__.setPlayedCount_(int(value))
        elif key == 'rating':
            self.__sb__.setRating_(int(value))
        elif key == 'comment':
            self.__sb__.setCommend_(comment)
        else:
            print 'Cannot set %s.' % key

    def __str__(self, sep=' - '):
        return sep.join(self.artist, self.album, self.name)

iTunes = ITunes(__app__)
