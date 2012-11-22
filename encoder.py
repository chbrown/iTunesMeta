#!/usr/bin/env python
# import os
import sys
# import subprocess
import re
# import time
from ScriptingBridge import SBApplication
iTunes = SBApplication.applicationWithBundleIdentifier_("com.apple.iTunes")
ws = re.compile(r'\s+')

def eachSBElementArray(sbElementArray):
    count = sbElementArray.count()
    for i in range(count):
        yield sbElementArray.objectAtIndex_(i)

def write_n(fp, s):
    fp.write(s.encode('utf8'))
    fp.write('\n')
    fp.flush()

def iterateTracks(fp):
    # new_state = PlayState(iTunes.currentTrack(), iTunes.playerPosition())
    first_source = eachSBElementArray(iTunes.sources()).next()
    first_library_playlist = eachSBElementArray(first_source.libraryPlaylists()).next()
    # iTunes.valueForKeyPath_("sources.@distinctUnionOfArrays.playlists.@distinctUnionOfArrays.tracks.name")
    # all_sources = list(eachSBElementArray(iTunes.sources()))
    # source = all_sources[0]
    # library_playlists = list(eachSBElementArray(source.libraryPlaylists()))
    # library_playlist = library_playlists[0]
    # playlists = iTunes.valueForKeyPath_("sources.playlists")
    headers = ['Artist', 'Album', 'Name', 'Played', 'Rating', 'Added', 'Comment']
    sep = '\t'
    write_n(fp, sep.join(headers))
    track_sb_array = first_library_playlist.tracks()
    # print track_array
    for track in eachSBElementArray(track_sb_array):
        # if track.rating() == 0:
            # continue
        cells = [
            track.artist(),
            track.album(),
            track.name(),
            track.playedCount(),
            track.rating(),
            track.dateAdded().timeIntervalSince1970(),
            track.comment()
        ]
        write_n(fp, sep.join(ws.sub(' ', unicode(cell)) for cell in cells))

# def main():
#     if iTunes.isRunning():
#     else:
#         print 'iTunes is not running'
# main()
iterateTracks(sys.stdout)
