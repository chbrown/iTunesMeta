#!/usr/bin/env python
# import os
import sys
from api import iTunes

def write_n(fp, s):
    fp.write(s.encode('utf8'))
    fp.write('\n')
    fp.flush()

library_cols = ['artist', 'album', 'name', 'plays', 'rating', 'added_ticks', 'comment']
playlist_cols = library_cols[:3]

def saveLibrary(sep='\t'):
    with open('Library.tsv', 'w') as fp:
        # write_n(fp, sep.join(library_cols))
        for track in iTunes.library.tracks:
            cells = [unicode(getattr(track, col)) for col in library_cols]
            write_n(fp, sep.join(cells))

def savePlaylists(sep='\t'):
    for playlist in iTunes.playlists(smart=False, basic=True):
        print 'Writing playlist', playlist
        with open('Playlist-%s.tsv' % playlist, 'w') as fp:
            for track in playlist.tracks:
                cells = [unicode(getattr(track, col)) for col in playlist_cols]
                write_n(fp, sep.join(cells))

def loadLibrary(sep='\t'):
    lookup = dict()
    for track_cells in open('Library.tsv'):
        track_values = dict(zip(library_cols, track_cells.split(sep)))
        track_key = '\t'.join([track_values['artist'], track_values['album'], track_values['name']])
        lookup[track_key] = track_values

    print 'Loaded %d tracks' % len(lookup)
    for track in iTunes.library.tracks:
        track_key = '\t'.join([track.artist, track.album, track.name])
        new_value = lookup.get(track_key)
        if new_value:
            print 'Setting %s to %s' % (track_key, new_value)
            # track.set
            # set plays


if __name__ == '__main__':
    loadLibrary()
