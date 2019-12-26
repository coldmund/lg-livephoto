import	argparse

def	main(recursive, path):
	print("main: {}, {}".format(recursive, path))
	if path==None:
		path = "."

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-r", "--recursive", help="search jpeg file recursively", action="store_true")
	parser.add_argument("-p", "--path", help="jpeg file search path")

	args = parser.parse_args()

	main(args.recursive, args.path)
