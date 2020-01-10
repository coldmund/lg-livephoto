import argparse
from pathlib import Path
import xml.etree.ElementTree as ET
import os

def	extIsJpeg(file):
	return	file.name.lower().endswith('.jpg')

def	read2Bytes(file):
	data = file.read(2)
	if data:
		return	int.from_bytes(data, byteorder='big')
	else:
		raise EOFError

# return:
#	0: OK
#	-1: not a jpeg file
#	-2: no XMP
#	-3: XMP error
def	processFile(file):
	print("processFile: {}".format(file.name))

	with open(file, 'rb') as f:
		# 1. check jpeg SOI
		if read2Bytes(f) != 0xffd8:
			print('	SOI not found')
			return	-1

		# 2. search for app1 marker
		xmpFound = False
		xmpStr = ''
		try:
			while xmpFound == False:
				while read2Bytes(f) != 0xffe1:
					pass
				# 3. search for XMP
				size = read2Bytes(f)
				data = ''
				try:
					data = f.read(size-2).decode('ascii')
					xmpStart = data.find('<x:xmpmeta')
					xmpEnd = data.find('</x:xmpmeta>')
					if xmpStart != -1 and xmpEnd != -1:
						xmpFound = True
						xmpStr = data[xmpStart:xmpEnd+12]
						# print('xmpStr: ', xmpStr)
				except:
					# print('	not ascii text')
					pass
		except EOFError:
			print('	EOF')
			return	-2

		# 4. parse xmp
		xmp = ET.fromstring(xmpStr)
		nmspdict = {
			'x': 'adobe:ns:meta/',
            'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'LGLivePic': 'http://ns.lge.com/gallery/1.0/livepicture/',
			'xmpNote': 'http://ns.adobe.com/xmp/note/',
			'LGBehindVideo': 'http://ns.lge.com/gallery/1.0/behindvideo/'}
		# print('xmp: ', ET.tostring(xmp))
		version = xmp.find('rdf:RDF/rdf:Description/LGLivePic:Version', namespaces=nmspdict)
		mime = xmp.find('rdf:RDF/rdf:Description/LGBehindVideo:Mime', namespaces=nmspdict)
		negOffset = xmp.find('rdf:RDF/rdf:Description/LGBehindVideo:NegativeOffset', namespaces=nmspdict)
		videoSize = xmp.find('rdf:RDF/rdf:Description/LGBehindVideo:Size', namespaces=nmspdict)
		if version is None or mime is None or negOffset is None or videoSize is None:
			print('	not my format')
			return	-3
		negOffset = int(negOffset.text)
		videoSize = int(videoSize.text)
		# print('negOffset: {}, videoSize: {}'.format(negOffset, videoSize))

		# 5. save files
		# print('dir: {}, name: {}'.format(file.parents[0], file.name))
		targetDir = file.parents[0].joinpath('output')
		movieFileName = file.name[: file.name.rfind('.')] + '.mp4'
		if not targetDir.exists():
			targetDir.mkdir()
		fileSize = os.path.getsize(file)
		f.seek(0)
		with open(targetDir.joinpath(file.name), 'wb') as jpegFile:
			jpegFile.write(f.read(fileSize - negOffset))
		f.seek(fileSize - negOffset)
		with open(targetDir.joinpath(movieFileName), 'wb') as movieFile:
			movieFile.write(f.read(videoSize))

		return	0

def	processDirectory(p):
	# print("processDir: {}".format(p.name))
	[processFile(file) for file in list(p.glob('*')) if file.is_file() and extIsJpeg(file)]
	[processDirectory(dir) for dir in p.iterdir() if (dir.is_dir() and dir.name != 'output')]

def	main(recursive, target):
	print("main: {}, {}".format(recursive, target))
	if target==None:
		target = "."

	p = Path(target)
	if p.is_file():
		processFile(p)
	elif recursive==True:
		processDirectory(p)
	else:
		[processFile(file) for file in list(p.glob('*')) if file.is_file() and extIsJpeg(file)]

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-r", "--recursive", help="search jpeg file recursively", action="store_true")
	parser.add_argument("-t", "--target", help="jpeg file search path")

	args = parser.parse_args()

	main(args.recursive, args.target)
