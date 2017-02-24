from __future__ import print_function
from MusicOrganizer import eprint
from MusicOrganizer import MusicOrganizer
import argparse
			
# ------------------------------ Main section ---------------------------------- #

# Setup argument parser
parser = argparse.ArgumentParser(
	description=('Audio file organizer. Recursively scans for audio files '
	'(supported formats: .flac, .mp3, .m4a) in a directory tree and organizes'
	' them under key which is constructed based on the audio file tags'
	' (i.e. <artist> - <album>{<year>}{[file_type>]}. It also gives the possibility'
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
	action='store_true',
	help='Print compiled database')
parser.add_argument('-s',
	metavar='file',
	help='Save compiled list into a pickle (.pkl) <file>')
parser.add_argument('-m',
	action='store_true',
	help=('Perform move (instead of copy) operation (only applicable if <dst> is'
	' specified)'))
parser.add_argument('-f',
	action='store_true',
	help=('Force directory merge: if a directory already exists in <dst> the files'
	' are going to be merged in it. If not specified the process skips the directory'
	' and continues with the next (if any).'))
args = parser.parse_args()

mo = MusicOrganizer()

# Handle src argument
if args.src.endswith('.pkl'):
	# TODO check if file exists
	mo.loadDB(args.src)
else:	
	# TODO check if a directory is given
	mo.scanDirTree(args.src)
	
# Handle -p option
if args.p:
	mo.printDB()

# Handle -s option
if args.s: 
	if not args.s.endswith('.pkl'):
		eprint('Error: Binary output file should be of \'pickle\' format (.plk)')
		exit()
	else:
		mo.saveDB(args.s)
	

exit()

# Check -c option
if args.c:
	outpath = args.c
	if os.path.exists(outpath):
		organizeFiles(db,outpath)
	else:
		eprint('Specified directory', ''.join(['\'',outpath,'\'']), 
			'does not exist. Please specify an existing directory and try again.')
		exit()
	
		



