import	argparse
from pathlib import Path

def	extIsJpeg(file):
	return	file.name.endswith('jpg') or file.name.endswith('jpeg')

# return:
#	-1: not a jpeg file
#	-2: no exif
#	-3: no XMD
#	-4: no movie data
def	processFile(file):
	print("processFile: {}".format(file.name))
	# 1. check jpeg(SOI)

	# 2. check exif

	# 3. find XMP

	# 4. save files

def	processDirectory(p):
	# print("processDir: {}".format(p.name))
	[processFile(file) for file in list(p.glob('*')) if file.is_file() and extIsJpeg(file)]
	[processDirectory(dir) for dir in p.iterdir() if dir.is_dir()]

def	main(recursive, path):
	print("main: {}, {}".format(recursive, path))
	if path==None:
		path = "."

	p = Path(path)
	if p.is_file():
		processFile(p)
	elif recursive==True:
		processDirectory(p)
	else:
		[processFile(file) for file in list(p.glob('*')) if file.is_file() and extIsJpeg(file)]

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-r", "--recursive", help="search jpeg file recursively", action="store_true")
	parser.add_argument("-p", "--path", help="jpeg file search path")

	args = parser.parse_args()

	main(args.recursive, args.path)
