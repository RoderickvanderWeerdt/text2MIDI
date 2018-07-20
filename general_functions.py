from os import walk
from os.path import join

def retrieve_files(path, file_extension):
	f = []
	for root, dirs, files in walk(path):
		for file in files:
			if file.lower().endswith(file_extension):
				f.append(join(root, file))
	return f

def retrieve_midi_files(path):
	return retrieve_files(path, ".mid")

def retrieve_lyric_bits_files(path):
	return retrieve_files(path, ".lyric_bits")

def retrieve_vector_files(path):
	return retrieve_files(path, ".vector")

def retrieve_vectors_files(path):
	return retrieve_files(path, ".vectors")
	
def retrieve_dirs(path):
	return next(walk(path))[1]