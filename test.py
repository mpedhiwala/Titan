print "Python Script to detect duplicate files"

import os.path
import hashlib
import glob
import pickle

hashMapFile = raw_input("Enter the hash map file");

hashMap = pickle.load(open (hashMapFile, 'rb'))

for hash in hashMap:
	# Get the set in this key ...
        duplicateSet = hashMap[hash]
	if len(duplicateSet) > 1:
        	print duplicateSet







