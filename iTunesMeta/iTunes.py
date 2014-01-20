from ScriptingBridge import SBApplication
app = SBApplication.applicationWithBundleIdentifier_('com.apple.iTunes')

import logging
logger = logging.getLogger(__name__)


ITunesPlaylist = app.classForScriptingClass_('playlist')

library_special_kinds = {
    1800630337: 'Audiobooks',
    1800630345: 'Movies',
    1800630348: 'Library',
    1800630349: 'Purchased',
    1800630352: 'Podcasts',
    1800630362: 'Music',
}


class SBWrapper(object):
    objc = None

    def __init__(self, objc):
        '''
        Initialize SBWrapper around raw object
        '''
        if objc is None:
            raise NotImplementedError('Cannot create a new SB object directly')
        self.objc = objc


def memoize(func):
    memoized_attr = '_' + func.__name__
    def wrapper(self, *args, **kw):
        # default to memoizable (memo=True)
        memoizable = kw.get('memo', True) is True
        memoized = hasattr(self, memoized_attr)
        # logger.critical('memoizable %s, memoized %s (%s, %s)', memoizable, memoized, args, kw)
        if memoizable and memoized:
            result = getattr(self, memoized_attr)
        else:
            result = func(self, *args, **kw)
            setattr(self, memoized_attr, result)
        return result
    return wrapper

class Source(SBWrapper):
    # self.objc is an instance of the ITunesSource ScriptingBridge class

    @classmethod
    def find(cls, name):
        '''
        Find a Source by `name`
        '''
        for source in app.sources():
            if source.name() == name:
                return cls(source)

        raise NotImplementedError('Cannot create a new ITunesSource')


    @memoize
    def user_playlists(self, **kw):
        # return list of Wrapped Track objects
        return [Playlist(playlist) for playlist in self.objc.userPlaylists()]

    @memoize
    def playlists(self, **kw):
        return [Playlist(playlist) for playlist in self.objc.playlists()]

    def find_or_create_playlist(self, name):
        '''
        Find or create Playlist by `name`
        '''
        # self.name = name
        # self.source = source
        for wrapped_playlist in self.playlists():
            if wrapped_playlist.objc.name() == name:
                return wrapped_playlist

        logger.warn('Creating playlist: %r', name)
        playlist = ITunesPlaylist.alloc().initWithProperties_(dict(name=name))
        self.objc.playlists().addObject_(self.objc)
        return Playlist(playlist)


class Playlist(SBWrapper):
    # self.objc is an instance of the ITunesPlaylist ScriptingBridge class

    def kind(self):
        # returns 'Library', 'Smart', or None (None denotes a basic/normal playlist)
        if self.objc.specialKind() in library_special_kinds:
            return 'Library'
        elif self.objc.smart():
            return 'Smart'
        # else:
            # assert special_kind_id == 1800302446, 'Unknown kind'

    @memoize
    def tracks(self, **kw):
        # return list of Wrapped Track objects
        return [Track(track) for track in self.objc.tracks()]

    def find_track(self, name):
        for wrapped_track in self.tracks():
            if wrapped_track.objc.name() == name:
                return wrapped_track


class Track(SBWrapper):
    # self.objc is an instance of the ITunesTrack ScriptingBridge class

    metadata_keys = [
        'playedCount',
        'playedDate',
        'skippedCount',
        'skippedDate',
        'rating',
        'dateAdded',
        'modificationDate',
    ]
    identifying_keys = [
        'album',
        'artist',
        'bitRate',
        'duration',
        'name',
        'persistentID',
        'size',
        'year',
    ]

    def properties(self):
        raw = self.objc.properties()
        return dict((key, raw[key]) for key in (self.metadata_keys + self.identifying_keys))

    def containing_playlists(self, playlists):
        # given a list of wrapped playlists, yields lists of (Playlist, Track) tuples
        persistentID = self.objc.persistentID()
        for playlist in playlists:
            for track in playlist.tracks():
                if track.objc.persistentID() == persistentID:
                    yield (playlist, track)
