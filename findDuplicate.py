import sys
sys.path.append ("/Users/mpedhiwala/github/local/Titan")
import thumbGen
import pymongo
import gridfs
from pymongo import Connection, ASCENDING

print "Python Script to detect duplicate files"

import os.path
import hashlib
import glob
import pickle
import socket

HOST_NAME = socket.gethostname();

FILE_EXTENSION = [".jpeg", ".JPG", ".jpg", ".JPEG"]

MONGO_HOST = '192.168.1.156'
connection = Connection (MONGO_HOST)
photo_db = connection.test
photo_collection = photo_db.photo_collection
photo_thumb_collection = gridfs.GridFS(photo_db, "photo_thumb_coll")


# Procedure to filter files based on extension
def filterFileTypes(filepath):
	name, ext = os.path.splitext(filepath)
	if ext in FILE_EXTENSION:
		return True
	else:
		return False

# Procedure to generate a thumbnail and save it in mongo
def saveThumbnailImg(filePath):
	_id = None
	print "Working on " + filePath
	(dir,fname) = os.path.split (filePath)
	dir = dir + os.sep
	if thumbGen.processTitanImage(dir, fname) == True:
		thumbFile = open (fname, 'r')
		_id = photo_thumb_collection.put(thumbFile, filename=fname)
		print "Deleteing thumbnail ..." + fname
		thumbFile.close()
		os.remove (fname)	
		
	return _id

# Calculate a md5 hash for the file ...
def md5sum(filename):
    md5 = hashlib.md5()
    with open(filename,'rb') as f:
        for chunk in iter(lambda: f.read(128*md5.block_size), b''): 
             md5.update(chunk)
    	f.closed
	return md5.hexdigest()
#end of procedure

# Find duplicate files ...
def findDuplicates (dirName):
	print "... finding duplicates in " + dirName + "\n"
	fileList = glob.glob(dirName + '/*')
	for file in fileList:
		if os.path.isdir(file): 
			findDuplicates(file)
		elif filterFileTypes(file):
			md5 = md5sum(file)
			
			# Generating a thumbnail and saving the thumbnail in mongo
			_thumbId = saveThumbnailImg(file)
			if _thumbId == None:
				continue
			print '... searching for the md5 hash in the Mongo Photo Collection'
			dup_photos = photo_collection.find_one({"file_hash":md5})
			if dup_photos is None:
				dup_photos = {"file_hash":md5, "files":[{"file":file, "host_name":HOST_NAME, "thumbId":_thumbId}]}
				photo_collection.insert (dup_photos)
			else:
				duplicateEntry = False
				for fileJSON in dup_photos["files"]:
					if (fileJSON["file"] == file) and (fileJSON["host_name"] == HOST_NAME):
						print "... found record"
						duplicateEntry = True
						break
				
				if duplicateEntry is False:
					dup_photos["files"].append({"file":file, "host_name":HOST_NAME, "thumbId":_thumbId});
				photo_collection.update ({"file_hash":md5},dup_photos)

def main():
	baseDir = ''
	baseDir = raw_input("Enter the base directory to search for duplicateFiles:")
	print "Will begin searching for duplicate files in " + baseDir;
	baseDir = os.path.abspath(baseDir);
	findDuplicates(baseDir)

if __name__ == "__main__":
	main()
