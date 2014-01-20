#!/usr/bin/env python
# import os
import re
import time
# import sys
from glob import glob
from api import iTunes
# from itertools import groupby
from collections import defaultdict


def write_n(fp, s):
    fp.write(s.encode('utf8'))
    fp.write('\n')
    fp.flush()

library_cols = ['artist', 'album', 'name', 'plays', 'rating', 'added_ticks', 'comment']
playlist_cols = library_cols[:3]


def saveLibrary(sep='\t'):
    with open('Library2.tsv', 'w') as fp:
        # write_n(fp, sep.join(library_cols))
        for track in iTunes.library.track_iter:
            cells = [unicode(getattr(track, col)) for col in library_cols]
            write_n(fp, sep.join(cells))


def savePlaylists(sep='\t'):
    for playlist in iTunes.playlists(smart=False, basic=True):
        print 'Writing playlist', playlist
        with open('Playlist-%s.tsv' % playlist, 'w') as fp:
            for track in playlist.track_iter:
                cells = [unicode(getattr(track, col)) for col in playlist_cols]
                write_n(fp, sep.join(cells))


def loadLibrary(sep='\t'):
    lookup = dict()  # track_key -> dict(track_values)
    for line in open('LibraryAir.tsv'):
        track_cells = line.replace('\n', '').decode('utf8')
        track_values = dict(zip(library_cols, track_cells.split(sep)))
        track_key = '\t'.join([track_values['artist'], track_values['album'], track_values['name']])
        # if track_key in lookup:
            # print 'Already stored', track_key, 'once'
        lookup[track_key] = track_values

    print 'Loaded %d tracks' % len(lookup)
    for track in iTunes.library.track_iter:
        track_key = '\t'.join([track.artist, track.album, track.name])
        new_value = lookup.get(track_key)
        if new_value:
            print 'Updating %s' % track_key.encode('utf8')

            # set rating
            old_rating = track.rating
            new_rating = int(new_value['rating'])
            if old_rating != new_rating:
                max_rating = max(old_rating, new_rating)
                track.set('rating', max_rating)
                print '  rating max(%d, %d) -> %d' % (old_rating, new_rating, max_rating)

            # set plays
            old_plays = track.plays
            new_plays = int(new_value['plays'])
            if old_plays != new_plays:
                sum_plays = old_plays + new_plays
                track.set('plays', sum_plays)
                print '  plays sum(%d, %d) -> %d' % (old_plays, new_plays, sum_plays)

            time.sleep(0.1)


def loadPlaylists(sep='\t'):
    lookup = dict()  # track_key -> api.Track
    for track in iTunes.library.track_iter:
        track_key = '\t'.join([track.artist, track.album, track.name])
        lookup[track_key] = track

    for playlist_tsv in glob('Playlist-*.tsv'):
        playlist_name = re.match('Playlist-(.+).tsv', playlist_tsv).group(1)
        print 'Creating playlist', playlist_name
        # continue
        playlist = iTunes.ensure_playlist(playlist_name)
        for line in open(playlist_tsv):
            track_cells = line.replace('\n', '').decode('utf8')
            track_values = dict(zip(playlist_cols, track_cells.split(sep)))
            track_key = '\t'.join([track_values['artist'], track_values['album'], track_values['name']])

            existing_track = lookup.get(track_key)
            if existing_track:
                playlist.add_track(existing_track)

                time.sleep(0.1)
            else:
                print 'Could not find:', track_key


def findDuplicates():
    duplicates = (p for p in iTunes.playlists(smart=False, basic=True) if p.name == 'Duplicates').next()

    lookup = defaultdict(list)  # track_key -> api.Track
    for track in iTunes.library.track_iter:
        track_key = '\t'.join([track.artist, track.album, track.name])
        lookup[track_key].append(track)

    for track_key, tracks in lookup.iteritems():
        if len(tracks) > 1:
            print len(tracks), track_key
            for track in tracks:
                duplicates.add_track(track)


def prioritizeDuplicates():
    duplicates = iTunes.ensure_playlist('Duplicates')

    lookup = defaultdict(list)  # track_key -> api.Track
    for track in duplicates.track_iter:
        track_key = '\t'.join([track.artist.lower(), track.name.lower()])
        lookup[track_key].append(track)

    for track_key, tracks in lookup.iteritems():
        if len(tracks) > 1:
            print len(tracks), track_key
            sorted_tracks = sorted(tracks, key=lambda t: -t.bitrate)

            sum_plays = sum(t.plays for t in tracks)
            max_rating = max(t.rating for t in tracks)
            print 'plays', sum_plays, 'rating', max_rating

            best_track = sorted_tracks[0]

            best_track.set('enabled', True)
            best_track.set('plays', sum_plays)
            best_track.set('rating', max_rating)

            time.sleep(0.1)

            for bad_track in sorted_tracks[1:]:
                bad_track.set('enabled', False)
                bad_track.set('plays', 0)
                bad_track.set('rating', 0)

                time.sleep(0.1)


if __name__ == '__main__':
    # findDuplicates()
    # prioritizeDuplicates()
    # loadLibrary()
    loadPlaylists()
