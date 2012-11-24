# Helpful links

http://www.mugginsoft.com/html/kosmictask/ScriptingBridgeDox/Apple/iTunes/OS-X-10.7/iTunes-10.6.1/html/interfacei_tunes_playlist.html
http://stackoverflow.com/questions/12964766/create-playlist-in-itunes-with-python-and-scripting-bridge
http://stackoverflow.com/questions/12971306/how-to-add-a-track-to-an-itunes-playlist-using-python-and-scripting-bridge

    from itertools import groupby
    all_ids = ['-'.join([track.artist(), track.album(), track.name()]) for track in all_tracks]

    playlists = list(eachSBElementArray(source.userPlaylists()))
    [(p.name(), p.shared(), p.smart()) for p in playlists]

    new_state = PlayState(iTunes.currentTrack(), iTunes.playerPosition())
    iTunes.valueForKeyPath_("sources.@distinctUnionOfArrays.playlists.@distinctUnionOfArrays.tracks.name")
    library_playlists = list(eachSBElementArray(source.libraryPlaylists()))
    library_playlist = library_playlists[0]

    def main():
        if iTunes.isRunning():
        else:
            print 'iTunes is not running'
