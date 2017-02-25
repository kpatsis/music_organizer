## Synopsis

Audio file organizer. Recursively scans for audio files (supported formats:
.flac, .mp3, .m4a) in a directory tree and compiles an organized list of where
every track in the tree is put under a key. The key is composed of the artist
tag followed by the album tag and optionally the year tag and the file type
(i.e. \<artist\> - \<album\> \{\<year\>\}\{\[\<file_type\>\]\}. It also gives the
possibility of creating directories (named with the aforementioned key) and
copy/move the original files into them.

## Dependencies

[`tinytag`](https://pypi.python.org/pypi/tinytag/) Python package

## Usage examples

```sh
# Scan a directory for audio files and print the organized list
python music_organizer /path/to/src_dir -p
```

## Contributors

For suggestions and bugs please email me at patsis.csd@gmail.com

## License

MIT License
