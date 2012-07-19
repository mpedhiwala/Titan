print "Python Script to detect duplicate files"

import os.path
import hashlib
import glob
import pickle

def md5sum(filename):
    md5 = hashlib.md5()
    with open(filename,'rb') as f: 
        for chunk in iter(lambda: f.read(128*md5.block_size), b''): 
             md5.update(chunk)
    return md5.hexdigest()

baseDir = '/Users/mpedhiwala/Pictures'

filename = '/Users/mpedhiwala/test.py'
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
			else:
				hashMap[md5] = set([file])	


findDuplicates(baseDir)

dictionaryFile = open ('duplicate.photos', 'wb')
pickle.dump(hashMap, dictionaryFile)



