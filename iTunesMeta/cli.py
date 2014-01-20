import sys
from iTunesMeta import serialization
from iTunesMeta.iTunes import Source

import logging
logger = logging.getLogger(__name__)

# from iTunesMeta.inspector import dump
# import IPython

# exit()

# self.position = position
# cols = [int(time.time()),
#     'Y' if last_state.position > (last_state.duration / 2.0) else 'N', last_state.position,
#     last_state.artist, last_state.album, last_state.track]
#     line = u'\t'.join(map(unicode, cols))
#     fp.write('%s\n' % line.encode('utf-8'))
#     fp.flush()
# return new_state

# last_state = None
# new_state = None
# log_path = os.path.join(os.environ['HOME'], '.iTunes_history')
# with open(log_path, 'a') as fp:
#     while True:
#         if iTunes.isRunning():
#             new_state = PlayState(iTunes.currentTrack(), iTunes.playerPosition())
#         else:
#             new_state = None
#         last_state = update(fp, last_state, new_state)
#         time.sleep(5)

def extract(parser):
    opts = parser.parse_args()
    library_source = Source.find('Library')

    # print summary of playlists
    # for playlist in library_source.playlists():
        # playlist is a wrapped Playlist
        # logger.info('Playlist %r has %d tracks', playlist.objc.name(), len(playlist.objc.tracks()))

    # testplaylist = find_or_create_playlist('testplaylist')
    # find Music playlist
    # for track in Music.tracks():
    #     if track.name().startswith('A'):
    #         logger.info('Adding track to testplaylist: %s', track.name())
    #         track.duplicateTo_(testplaylist)

    music_playlist = library_source.find_or_create_playlist('Music')
    music_tracks = music_playlist.tracks()

    # for playlist in playlists:
        # print '%r : %s' % (playlist.objc.name(), playlist.kind())
    # deine_track = music_playlist.find_track('Deine Distanz')
    # for  in deine_track.:
    #     print playlist.objc.name(), track.objc.name(), track.objc.index()

    # sami_playlist = library_source.find_or_create_playlist('Sami')
    # sami_deine = sami_playlist.find_track('Deine Distanz')

    static_playlists = [playlist for playlist in library_source.user_playlists() if playlist.kind() is None]
    # pls0 = static_playlists[0]
    # print pls0.objc.properties()
    # IPython.embed(); raise SystemExit(98)
    for i, track in enumerate(music_tracks):
        # each track is a wrapped Track instance
        metadata = track.properties()
        metadata['playlists'] = dict((playlist.objc.name(), track.objc.index()) for playlist, track in track.containing_playlists(static_playlists))

        opts.output.write(serialization.jsonize(metadata))
        opts.output.write('\n')
        opts.output.flush()

        sys.stderr.write('\r% 6.2f%%' % (100.0 * (i + 1.0) / len(music_tracks)))
        sys.stderr.flush()
    logger.info('Done!')


def main():
    import argparse
    commands = dict(extract=extract)
    parser = argparse.ArgumentParser(description='iTunesMeta CLI',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('command', choices=commands, help='Command to run')
    parser.add_argument('--output', nargs='?', type=argparse.FileType('w'), default=sys.stdout,
        help='Output JSON destination (defaults to STDOUT)')
    parser.add_argument('--verbose', action='store_true', help='Log detailed output')
    opts, _ = parser.parse_known_args()

    level = logging.DEBUG if opts.verbose else logging.INFO
    logging.basicConfig(level=level)
    logger.debug('logger level = %d', logger.level)

    commands[opts.command](parser)


if __name__ == '__main__':
    main()
