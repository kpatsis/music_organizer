from __future__ import print_function
import os
import sys
import shutil
import pickle
from tinytag import TinyTagException
from tinytag import TinyTag

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128 and ord(i)>0)

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class MusicOrganizer:
	
	def __init__(self, db={}, show_year=False, show_type=True):
		self.db = db
		self.show_year = show_year
		self.show_type = show_type
		
	def saveDB(self, filename):
		with open(filename, 'wb') as f:
			pickle.dump(self.db, f, pickle.HIGHEST_PROTOCOL)

	def loadDB(self, filename):
		with open(filename, 'rb') as f:
			self.db = pickle.load(f)
			
	def setDirNameOptions(self, show_year=False, show_type=True):
		self.show_year = show_year
		self.show_type = show_type
		    
	def printDB(self,filename=None):
		if filename == None:
			f = sys.stdout
		else:
			f = open(filename, 'w')
			
		for key in self.db.keys():
			print(key, end='\n', file=f)			
			for elem in sorted(self.db[key]):
				if isinstance(elem, basestring):
					print('\t', elem, end='\n', file=f)
				else:
					raise Exception('Wrong DB format: non-string elements are not allowed.')
					return
							
		if filename != None:
			f.close()
			
	def constructDirName(self,filename):
		tag = TinyTag.get(filename)
		dirname = []
		
		artist_tag = removeNonAscii(tag.artist).strip(' ,')
		album_tag = removeNonAscii(tag.album).strip(' ,')
		dirname.append(''.join([artist_tag,' - ',album_tag]))
		
		if self.show_year and tag.year:
			year_tag = removeNonAscii(tag.year).strip(' ,')
			dirname.append(''.join([' (',year_tag,')']))
		
		if self.show_type:
			ext = os.path.splitext(filename)[1][1:].upper()
			if ext != 'MP3':
				dirname.append(''.join([' [',ext,']']))		
			
		return ''.join(dirname).strip()
				 
			
	def scanFile(self, filename):
		if filename.endswith('.m4a') or filename.endswith('.mp3') or filename.endswith('.flac'):
			print('Reading file:', ''.join(['\'',filename,'\'']))
			ret = -1
			
			try:
				dirname = self.constructDirName(filename)
				if self.db.has_key(dirname):
					seen = set(self.db[dirname])
					if filename not in seen:
						self.db[dirname].append(filename)
						ret = 0
					else:
						ret = 1
				else:
					self.db[dirname] = [filename]
					ret = 0			
			except TinyTagException as err:
				eprint('Tag Error:', err)
			#except Exception as e:
			#	eprint('Error:', str(e), '>file:', filename)
	
			return ret
		else:
			return -1
			
	def scanDirTree(self, path):
		for root, dirs, files in os.walk(path):
			for elem in files:
				self.scanFile(os.path.join(root,elem))
			
	def organizeFiles(self, outpath, force_dir_merge=False, move=False):
		for key in self.db.keys():
			dirpath = os.path.join(outpath,key)
			
			if not os.path.exists(dirpath):
				print('Creating directory', ''.join(['\'',dirpath,'\'.']))
				os.makedirs(dirpath)
			elif force_dir_merge:
				print('Entering directory', ''.join(['\'',dirpath,'\'.']))
			else:
				eprint('Warning: directory ', ''.join(['\'',dirpath,'\'']), 
					('already exists. To ensure that no data is being overwritten, '
					'this directory is skipped.') )
				continue
				
			for elem in self.db[key]:
				# prepare filename
				filename = removeNonAscii(os.path.split(elem)[1])
				fullpath = os.path.join(dirpath,filename)
				if move:
					print('Moving', ''.join(['\'',elem,'\'']), 'to', 
						''.join(['\'',dirpath,'\'.']))				
					shutil.move(elem,fullpath)
				else:				
					print('Copying', ''.join(['\'',elem,'\'']), 'to', 
						''.join(['\'',fullpath,'\'.']))				
					shutil.copy2(elem,fullpath)

