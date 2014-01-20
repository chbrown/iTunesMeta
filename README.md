# iTunesMeta

Moving files between iTunes libraries is fraught with potential data loss because only the music files that may be transfered, yet a considerable amount of the data pertaining to your library is not stored in the music files themselves.

This data, which must be transferred by some other mechanism, I call "metadata".

## Extraction

This project currently extracts an iTunes library into a json file, each line a single document, corresponding to a music track in the iTunes library.

```sh
itunes-meta extract
```

Run `itunes-meta --help` to show all options.


### Schema

The following properties are pulled directly (while formatting dates as ISO strings) from the ScriptingBridge's `ITunesTrack` representation:

- playedCount
  * `int`: Defaults to zero
- playedDate
  * `unicode`: ISO-8601 format without microseconds or timezone
- skippedCount
  * `int`: Defaults to zero
- skippedDate
  * `unicode`: ISO-8601 format without microseconds or timezone
- rating
  * `int`: iTunes' internal representation is the number of stars * 20, so the range of rating is 0 to 100, inclusive
- dateAdded
  * `unicode`: ISO-8601 format without microseconds or timezone
- modificationDate
  * `unicode`: ISO-8601 format without microseconds or timezone

The `playlists` property is not a feature of the track directly, but of the playlists it is in.

- playlists
  * `dict(unicode -> int)`: Mapping from playlist name to index of the track in the corresponding playlist.

A few other fields are extracted to be used to link the music data back to the file in the other library.

(WXYZ) denotes an ID3v2 tag.

- album (TALB)
- artist (TPE1)
- bitRate (property of the audio encoding)
- duration (property of the audio encoding)
- name (TIT2)
- persistentID
  * I'm not sure if this is actually persisted inside the MP3; it is not in embedded plaintext, at least, and doesn't show up in IDv3
- size (file size)
- year (TYER)


## Ignored metadata:

Rare or not very useful variables include:

- bookmark
- bookmarkable
- category
- compilation
- databaseID
- enabled
- EQ
- finish
- gapless
- grouping
- id
- index
- iTunesU
- kind
- longDescription
- lyrics
- objectDescription
- podcast
- releaseDate
- sampleRate
- seasonNumber
- show
- shufflable
- sortAlbum
- sortAlbumArtist
- sortArtist
- sortComposer
- sortName
- sortShow
- time (derivative of duration)
- unplayed (same as playedCount == 0)
- videoKind
- volumeAdjustment

The following are (usually?) stored in the MP3's IDv3 (v1 and/or v2) database.

- bpm (TBPM)
- comment (COMM)
- composer (TCOM)
- discCount (TPOS)
- discNumber (TPOS)
- genre
- trackCount (TRCK)
- trackNumber (TRCK)


# Helpful links

- http://www.mugginsoft.com/html/kosmictask/ScriptingBridgeDox/Apple/iTunes/OS-X-10.7/iTunes-10.6.1/html/interfacei_tunes_playlist.html
- http://stackoverflow.com/questions/12964766/create-playlist-in-itunes-with-python-and-scripting-bridge
- http://stackoverflow.com/questions/12971306/how-to-add-a-track-to-an-itunes-playlist-using-python-and-scripting-bridge


## License

Copyright © 2013–2014 Christopher Brown. [MIT Licensed](LICENSE).
