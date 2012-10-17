# Thumbnail generation
import os
import sys
import Image
from PIL import Image
from PIL.ExifTags import TAGS
 
albumdir = 'album'
thumbdir = albumdir + '/thumbs'
 
def mkdir(dirname):
	try:
		os.mkdir(dirname)
	except:
		pass
 
def maxSize(image, maxSize, method = 3):
	imAspect = float(image.size[0])/float(image.size[1])
	outAspect = float(maxSize[0])/float(maxSize[1])
 
	if imAspect >= outAspect:
		return image.resize((maxSize[0], int((float(maxSize[0])/imAspect) + 0.5)), method)
	else:
		return image.resize((int((float(maxSize[1])*imAspect) + 0.5), maxSize[1]), method)



def processTitanImage(imgdir, fname):
    
	exif = None
	img = None
	
	try:
		img = Image.open(imgdir + fname)
	except:
		return False
		
	exif = img._getexif()
	
	if exif != None:
		for tag, value in exif.items():
			decoded = TAGS.get(tag, tag)
			if decoded == 'Orientation':
				if value == 3: img = img.rotate(180)
				if value == 6: img = img.rotate(270)
				if value == 8: img = img.rotate(90)
				break
	img = maxSize(img, (1024, 768), Image.ANTIALIAS)
	#img.save(albumdir + '/' + fname, 'JPEG', quality=100)
	img.thumbnail((192, 192), Image.ANTIALIAS)
	img.save(fname, 'JPEG')
	return True
 
def processImage(imgdir, fname):
	img = Image.open(imgdir + fname)
	exif = img._getexif()
	if exif != None:
		for tag, value in exif.items():
			decoded = TAGS.get(tag, tag)
			if decoded == 'Orientation':
				if value == 3: img = img.rotate(180)
				if value == 6: img = img.rotate(270)
				if value == 8: img = img.rotate(90)
				break
	img = maxSize(img, (1024, 768), Image.ANTIALIAS)
	img.save(albumdir + '/' + fname, 'JPEG', quality=100)
	img.thumbnail((192, 192), Image.ANTIALIAS)
	img.save(thumbdir + '/' + fname, 'JPEG')
 
def main():
	if len(sys.argv) < 2:
		print "Usage: album.py imgdir"
		exit(0)
	else:
		imgdir = sys.argv[1] + '/'
 
	mkdir(albumdir)
	mkdir(thumbdir)
	files = os.listdir(imgdir)
 
	for fname in files:
		if fname.lower().endswith('.jpg'):
			processImage(imgdir, fname)
 
	print 'done'
 
if __name__ == "__main__":
	main()

