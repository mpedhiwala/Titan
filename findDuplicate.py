#
print "Python Script to detect duplicate files"

import os.path
import hashlib
import glob
import pickle

def md5sum(filename):
    hex_digest=''
    md5 = hashlib.md5()	
    with open(filename,'rb') as f: 
        for chunk in iter(lambda: f.read(128*md5.block_size), b''): 
             md5.update(chunk)
        hex_digest = md5.hexdigest()
	f.close()
	
	return hex_digest

baseDir = ''

baseDir = raw_input("Enter the base directory to search for duplicateFiles:")


print "Will begin searching for duplicate files in " + baseDir;

hashMap = {}

def findDuplicates (dirName):
	print "... finding duplicates in " + dirName + "\n"
	fileList = glob.glob(dirName + '/*')
	for file in fileList:
		if os.path.isdir(file): 
			findDuplicates(file)
		else:
			md5 = md5sum(file)
			if md5 in hashMap:
				hashMap[md5].add(file)
			elif md5 is not '':
				hashMap[md5] = set([file])	


				

findDuplicates(baseDir)

outputFileName = '_'.join( baseDir.split(os.sep)) + ".dupPhotos"

print "Writing hashMap to " + outputFileName 

dictionaryFile = open (outputFileName, 'wb')
pickle.dump(hashMap, dictionaryFile)

