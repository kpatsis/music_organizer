from __future__ import print_function
from MusicOrganizer import eprint
from MusicOrganizer import MusicOrganizer
import argparse
import os
		

# Setup argument parser
parser = argparse.ArgumentParser(
	description=('Audio file organizer. Recursively scans for audio files '
	'(supported formats: .flac, .mp3, .m4a) in a directory tree and compiles'
	' an organized list of where every track in the tree is put under a key.'
	' The key is composed of the artist tag followed by the album tag and'
	' optionally the year tag and the file type'
	' (i.e. <artist> - <album> {<year>}{[<file_type>]}. It also gives the possibility'
	' of creating directories (named with the aforementioned key) and copy/move'
	' the original files into them.'))
parser.add_argument('src',
	help=('Either the path of a directory to be scanned for audio files or'
	' a .pkl file containing a previously compiled database (with the \'-s\' option)'))
parser.add_argument('dst',
	nargs='?',
	default=None,
	help=('Path of the destination directory. If provided, the compiled database is '
	'realized in the specified destination. By default, the audio files in <src> are'
	' copied to the appropriately named directory inside <dst> directory.'
	' Use option -m to move (instead of copy) the files to the destination. If not'
	' provided, no new files/directories are created.'))
parser.add_argument('-p',
	metavar='file',
	nargs='?',
	const=None,
	default='',
	help='Print compiled database. If a file is specified the database is written in it.')
parser.add_argument('-s',
	metavar='file',
	help='Save compiled list into a pickle (.pkl) <file>')
parser.add_argument('-m',
	action='store_true',
	help=('Perform move (instead of copy) operation. Only applicable if <dst> is'
	' specified.'))
parser.add_argument('-f',
	action='store_true',
	help=('Force directory merge: if a directory already exists in <dst> the files'
	' are going to be merged in it. If not specified the process skips the directory'
	' and continues with the next (if any). . Only applicable if <dst> is'
	' specified.'))
parser.add_argument('-y',
	action='store_true',
	help=('Include year tag in the key name. Only valid if <src> is a directory:'
	' if the database is loaded from a .pkl'
	' file, the key names already defined in there are going to be used.'))
parser.add_argument('-t',
	action='store_true',
	help=('Include file type tag in the key name. This will be done only if the files'
	' under that key are non .mp3 (.flac or .m4a).'
	' Only valid if <src> is a directory: if the database is loaded from a .pkl'
	' file, the key names already defined in there are going to be used.'))
args = parser.parse_args()

# Create MusicOrganizer instance
mo = MusicOrganizer()

# Handle -y and -t options
mo.setDirNameOptions(show_year=args.y, show_type=args.t)

# Handle src argument
if os.path.isfile(args.src) and args.src.endswith('.pkl'): 
	mo.loadDB(args.src)
elif os.path.isdir(args.src):
	mo.scanDirTree(args.src)
else:
	eprint('Error: Source can either be a .pkl file or a directory')
	
# Handle -p option
# TODO fix print option. when not used it is still being printed
if args.p != '':
	mo.printDB(args.p)

# Handle -s option
if args.s: 
	if not args.s.endswith('.pkl'):
		eprint('Error: Output file should have .plk extension')
		exit()		
	else:
		mo.saveDB(args.s)
		
# Handle dst argument
if args.dst:
	if os.path.isdir(args.dst):
		mo.organizeFiles(args.dst)
	else:
		eprint('Error: Specified destination does not exist of is not a directory')
		exit()


