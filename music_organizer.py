from __future__ import print_function
import os
import sys
import tinytag
import pickle
import argparse
from tinytag import TinyTag
import shutil

# ------------Function definition section--------------------#

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128 and ord(i)>0)

def saveDB(db,filename):
    with open(filename, 'wb') as f:
        pickle.dump(db, f, pickle.HIGHEST_PROTOCOL)

def loadDB(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def scanToDB(path,db):
	for root, dirs, files in os.walk(path):
		for elem in files:
			if elem.endswith('.m4a') or elem.endswith('.mp3') or elem.endswith('.flac'):
				print('Reading file:', ''.join(['\'',os.path.join(root,elem),'\'']))
				try:
					tag = TinyTag.get(os.path.join(root,elem))
					artist = removeNonAscii(tag.artist).strip(' ,')
					album = removeNonAscii(tag.album).strip(' ,')
					key = ''.join([artist,' - ',album])
					if db.has_key(key):
						db[key].append(os.path.join(root,elem))
					else:
						db[key] = [os.path.join(root,elem)]
				except tinytag.TinyTagException as err:
					eprint('Tag Error:', err)
				except Exception as e:
					eprint('Error:', str(e), '>file:', elem)

#def scanToDB_old(path,filename,db):
#	if filename.endswith('.m4a') or filename.endswith('.mp3') or filename.endswith('.flac'):
#		try:
#			tag = TinyTag.get(os.path.join(path,filename))
#			artist = removeNonAscii(tag.artist).strip(' ,')
#			album = removeNonAscii(tag.album).strip(' ,')
#			key = ''.join([artist,' - ',album])
#			if db.has_key(key):
#				db[key].append(os.path.join(path,filename))
#			else:
#				db[key] = [os.path.join(path,filename)]
#		except tinytag.TinyTagException as err:
#			eprint('Tag Error:', err)
#		except Exception as e:
#			eprint('Error:', str(e), 'file:', elem)
			
def organizeFiles(db,outpath):
	for key in db.keys():
		dirpath = os.path.join(outpath,key)
		if os.path.exists(dirpath):
			eprint('Warning: directory ', ''.join(['\'',dirpath,'\'']), 'already exists. To ensure that no data is being overwritten, this directory is skipped.')
			continue
		else:
			print('Creating directory', ''.join(['\'',dirpath,'\'.']))
			os.makedirs(dirpath)
			for elem in db[key]:
				# prepare filename
				filename = removeNonAscii(os.path.split(elem)[1])
				print('Copying', ''.join(['\'',elem,'\'']), 'to', ''.join(['\'',os.path.join(dirpath,filename),'\'.']))				
				shutil.copy2(elem,os.path.join(dirpath,filename))
			
def printDB(db):
	for key in db.keys():
		print(key)
		for elem in sorted(db[key]):
			print('\t',elem)
			
# -------------------Main section----------------------------#

# Setup argument parser
parser = argparse.ArgumentParser(description='Audio file organizer. Recursively scans for audio files (supported formats: .flac, .mp3, .m4a) in the specified folder and organizes them according to the \'artist\' and \'album\' tag.')
parser.add_argument('path',help='Path of the directory to scan for audio files. If the \'-b\' option is used, the list is loaded directly from the binary file (.plk)')
parser.add_argument('-p',action='store_true',help='Print organized audio file list')
parser.add_argument('-b',action='store_true',help='Don\'t scan directory but load the organized list from a previously created (with \'-s\' option) binary file (.plk)')
parser.add_argument('-s',metavar='file',help='Save organized list into a pickle <file>')
parser.add_argument('-c',metavar='dir',help='Create directories in <dir> according to the organized list and copy the appropriate audio files in it. <dir> must exist')
args = parser.parse_args()
#parser.print_help()
#print(args)

# Create empty DB dictionary
db = {}
		
# Check -b option	
if args.b: # Read from .plk file
	if not args.path.endswith('.pkl'):
		eprint('binary input file should be of \'pickle\' format (.plk)')
		exit()
	else:
		db = loadDB(args.path)
else: # Scan given directory
	if os.path.exists(args.path):
		scanToDB(args.path,db)
	else:
		eprint('Specified directory', ''.join(['\'',args.path,'\'']), 'does not exist. Please specify an existing directory and try again.')
	

# Check -s option
if args.s: 
	if not args.s.endswith('.pkl'):
		eprint('binary output file should be of \'pickle\' format (.plk)')
		exit()
	else:
		saveDB(db,args.s)

# Check -p option
if args.p:
	printDB(db)

# Check -c option
if args.c:
	outpath = args.c
	if os.path.exists(outpath):
		organizeFiles(db,outpath)
	else:
		eprint('Specified directory', ''.join(['\'',outpath,'\'']), 'does not exist. Please specify an existing directory and try again.')
	
		



