from __future__ import print_function
import os
import sys
import pickle
from tinytag import TinyTagException
from tinytag import TinyTag

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128 and ord(i)>0)

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class MusicOrganizer:
	ARTIST = 'a'
	ALBUM = 'n'
	YEAR = 'y'
	TYPE = 't'
	COMPONENTS = [ARTIST,ALBUM,YEAR,TYPE] 
	
	def __init__(self, db={}):
		self.db = db
		self.dirname_style = 'anyt'
		
	def saveDB(self, filename):
		with open(filename, 'wb') as f:
			pickle.dump(self.db, f, pickle.HIGHEST_PROTOCOL)

	def loadDB(self, filename):
		with open(filename, 'rb') as f:
			self.db = pickle.load(f)
		    
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
		sl = list(self.dirname_style)
		dirname = []
		options = {'a':True,'n':True,'y':False,'t':False}
		
		for component in sl:
			if component in self.COMPONENTS:
				options[component] = True
		
		if options['a']: 
			artist_tag = removeNonAscii(tag.artist).strip(' ,')
			dirname.append(''.join([artist_tag,' - ']))
		
		if options['n']:
			album_tag = removeNonAscii(tag.album).strip(' ,')
			dirname.append(''.join([album_tag,' ']))
		
		if options['y']:
			if tag.year:
				year_tag = removeNonAscii(tag.year).strip(' ,')
				dirname.append(''.join(['(',year_tag,')',' ']))
		
		if options['t']:
			ext = os.path.splitext(filename)[1][1:].upper()
			if ext != 'MP3':
				dirname.append(''.join(['[',ext,']']))		
			
		return ''.join(dirname).strip()
				 
			
	def scanDirTree(self, path):
		for root, dirs, files in os.walk(path):
			for elem in files:
				self.scanFile(os.path.join(root,elem))
				
						
	def scanFile(self, filename):
		if filename.endswith('.m4a') or filename.endswith('.mp3') or filename.endswith('.flac'):
			print('Reading file:', ''.join(['\'',filename,'\'']))
			ret = -1
			
			#try:
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
			#except TinyTagException as err:
			#	eprint('Tag Error:', err)
			#except Exception as e:
			#	eprint('Error:', str(e), '>file:', filename)
	
			return ret
		else:
			return -1

		    
mo = MusicOrganizer()

mo.scanDirTree('/media/Data/organized music')

mo.printDB('folderlist.txt')
