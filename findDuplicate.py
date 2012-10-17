import os,sys
#sys.path.append ("/Users/mpedhiwala/github/local/Titan")
import thumbGen
import pymongo
import gridfs
from pymongo import Connection, ASCENDING
from stat import *


print "Python Script to detect duplicate files"

import os.path
import hashlib
import glob
import pickle
import socket

HOST_NAME = socket.gethostname();

FILE_EXTENSION = [".jpeg", ".JPG", ".jpg", ".JPEG"]

MONGO_HOST = '192.168.1.146'
connection = Connection (MONGO_HOST)
photo_db = connection.test
photo_collection = photo_db.photo_collection
photo_thumb_collection = gridfs.GridFS(photo_db, "photo_thumb_coll")
processed_files = photo_db.processed_files


def isProcessedFile(filePath):
	(path, fname) = os.path.split(filePath)
	name, ext = os.path.splitext(filePath)
	st_mtime = os.stat(filePath).st_mtime
	st_size  = os.stat(filePath).st_size
	st_ino   = os.stat(filePath).st_ino
	collection_query =  {'host':HOST_NAME, 'path':path, 'st_mtime':st_mtime, 'st_ino':st_ino, 'st_size':st_size, 'fname':fname}
	stat_details = processed_files.find_one({'host':HOST_NAME, 'path':path, 'st_mtime':st_mtime, 'st_ino':st_ino, 'st_size':st_size, 'fname':fname});
	if stat_details is None:
		return (False, collection_query)
	else:
		return (True, None)	
	
# Procedure to filter files based on extension
def filterFileTypes(filepath):
	name, ext = os.path.splitext(filepath)
	if ext in FILE_EXTENSION:
		return True
	else:
		return False

# Procedure to generate a thumbnail and save it in mongo
def saveThumbnailImg(filePath):
	print "... creating thumbnail image for " + filePath
	(dir,fname) = os.path.split (filePath)
	dir = dir + os.sep
	thumbGen.processTitanImage(dir, fname) 
	thumbFile = open (fname, 'r')
	_id = photo_thumb_collection.put(thumbFile, filename=fname)
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
def findDuplicates(dirName):
	
	print "... finding duplicates in " + dirName + "\n"

	try:	
		fileList = glob.glob(dirName + '/*')
	except:
		print "An unexpected exception occurred"
		return
 
	for file in fileList:
	
		if os.path.isdir(file): 
			findDuplicates(file)
		elif filterFileTypes(file):
			isProcessed, stats_details = isProcessedFile(file)
			if isProcessed is True:
				print "..." + file + " has already been processed"
				continue;
		
			md5 = md5sum(file)
			
			# Generating a thumbnail and saving the thumbnail in mongo
			_thumbId = saveThumbnailImg(file)
			
			print '... searching for the md5 hash in the Mongo Photo Collection'
			dup_photos = photo_collection.find_one({"file_hash":md5})
			if dup_photos is None:
				dup_photos = {"file_hash":md5, "files":[{"file":file, "host_name":HOST_NAME, "thumbId":_thumbId}]}
				photo_collection.insert (dup_photos)
			else:
				dup_photos["files"].append({"file":file, "host_name":HOST_NAME, "thumbId":_thumbId});
				photo_collection.update ({"file_hash":md5},dup_photos)

			processed_files.insert(stats_details)
	
	#end of for loop

#end of findDuplicates

def main():

	baseDir = ''
	baseDir = raw_input("Enter the base directory to search for duplicateFiles:")
	print "Will begin searching for duplicate files in " + baseDir;
	baseDir = os.path.abspath(baseDir);
	findDuplicates(baseDir)

#end of main()

if __name__ == "__main__":
	main()
>>>>>>> Stashed changes
