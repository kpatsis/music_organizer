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

# Scan a directory for audio files and write the organized list in a file
python music_organizer /path/to/src_dir -p filename.txt

# Scan a directory for audio files and include the year tag in the directory name
python music_organizer /path/to/src_dir -p -y

# Scan a directory for audio files and save the internal database to a .pkl file
python music_organizer /path/to/src_dir -s db.pkl

# Load a database from a .pkl file and print it
python music_organizer /path/to/db.pkl -p

# Scan a directory for audio files and copy them in an organized manner into a directory
python music_organizer /path/to/src_dir /path/to/dst_dir

# Move, instead of copy, the files
python music_organizer /path/to/src_dir /path/to/dst_dir -m
```

## Contributors

For suggestions and bugs please email me at patsis.csd@gmail.com

## License

MIT License
