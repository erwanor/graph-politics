import os

def read_file(path):
	"""
	Read file at `path`.
	Return a list of lines
	"""
	lines = []
	with open(path, 'r') as srcfile:
		return srcfile.read().split('\n')

def get_crd(exc_file):
	return os.path.dirname(os.path.realpath(exc_file))

def get_path(current, path_to):
	return ''.join([current, path_to])
