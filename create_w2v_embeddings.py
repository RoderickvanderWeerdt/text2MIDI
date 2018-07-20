import gensim
from gensim.models import word2vec as w2v
from os.path import exists
import numpy as np

from process_lyrics import clean_lyrics

#if an model is found it is loaded, otherwise a new model is created
#from the datafile, make_new forces a new model to be created, regardless 
#of any already existing model.
def create_model(data_file, model_file, make_new=False, size=100, window=3, min_count=5):
	if not exists(model_file) or make_new:
		print("creating new model...")
		sentences = w2v.LineSentence(data_file)
		model = w2v.Word2Vec(sentences, size=size, window=window, min_count=min_count, workers=4)
		model.save(model_file)
	else:
		print("loading existing model...")
		model = w2v.Word2Vec.load(model_file)
	return model

#creates a vector for an entity (either song or input text)
#by averaging all the words in the entity
def create_entity_vector(model, words):
	entity_vec = 0
	word_vecs = []
	for word in words:
		try:
			word_vecs.append(model.wv[word])
		except:
			#word not recognized
			pass

	#method 1
	try:
		entity_vec = np.average(np.matrix(word_vecs), axis=0)
	except:
		return [0]
	#TODO: implement different methods?

	return entity_vec.tolist()[0]

def printable_vec(vector):
	printable = ""
	for number in vector:
		printable += str(number) + ','
	printable = printable[:-1] + '\n' #remove last ',' and add \n
	return printable

#creates a vector for each song, as retrieved from lyrics_txt with the use of index_txt
#all the new songvectors are saved in the newly created song_vectors_file
def create_entity_vectors(model, lyrics_txt, index_txt, song_vectors_file):
	with open(lyrics_txt, 'r') as lyrics_doc:
		with open(index_txt, 'r') as index_doc:
			with open(song_vectors_file, 'w') as vector_doc:
				index_lines = index_doc.readlines()
				pointer = 0
				for line in index_lines:
					song_id, index_begin, index_end = line.split(';')[:3]
					words = []
					while pointer < int(index_end):
						line = lyrics_doc.readline()
						words += line.split()
						pointer += 1
					entity_vec = create_entity_vector(model, words)
					vector_doc.write(song_id + ';' + printable_vec(entity_vec) + '\n')

def create_test_entity(model, lyrics_txt):
	words = []
	with open(lyrics_txt, 'r') as lyrics_doc:
		for line in lyrics_doc.readlines():
			words += line.split()
	entity_vec = create_entity_vector(model, words)
	return entity_vec

# creates vectors for one file containing lyrics, vectors 
# are created using sequences of sentences shorter then 140 characters.
def create_test_entities(model_filename, lyrics_txt):
	model = w2v.Word2Vec.load(model_filename)
	lyric_bits = [] #only text
	with open(lyrics_txt, 'r') as lyrics_doc:
		clean_lyric = clean_lyrics(lyrics_doc.read(), False)
		pointer = 0
		for line in clean_lyric.split('\n'):
			if len(line) > 140:
				line = line[:140]
			lyric_bits.append("")
			for i, lyric_bit in enumerate(lyric_bits):
				if i >= pointer:
					if len(lyric_bit) + len(line) <= 140:
						if lyric_bits[i] != "":
							lyric_bits[i] += " "
						lyric_bits[i] += line
					else:
						pointer += 1

	vectors = []
	for lyric_bit in lyric_bits:
		vectors.append(create_entity_vector(model, lyric_bit.split()))
	return vectors

# creates vectors for one file containing lyrics, 
# only one vector is created using the entire text.
def create_single_entity(model_filename, lyrics_txt):
	model = w2v.Word2Vec.load(model_filename)
	lyric_bit = "" #only text
	with open(lyrics_txt, 'r') as lyrics_doc:
		clean_lyric = clean_lyrics(lyrics_doc.read(), False)
		for line in clean_lyric.split('\n'):
			lyric_bit += line + " "
	lyric_bit = lyric_bit[:-1] #remove last " "

	# vector = [create_entity_vector(model, lyric_bit.split())]
	return [create_entity_vector(model, lyric_bit.split())]

class LyricBit:
	def __init__(self):
		self.text = ""
		self.identifier = False

#returns lyric_bits from a given .lyric_bits file, so the texts
#in the file can be used.
def get_lyric_bits(lyrics_bits_filename):
	lyric_bits = [LyricBit()]
	with open(lyrics_bits_filename, 'r') as lyrics_bits_file:
		for lyric_bit in lyrics_bits_file:
			lines = lyric_bit.split('\r')
			for line in lines:
				line = line.replace('\r', '')
				if line.startswith("TICK"):
					lyric_bits[-1].identifier = line[line.find('_', 10)+1:]
					lyric_bits.append(LyricBit())
				else:
					lyric_bits[-1].text += line
	lyric_bits = lyric_bits[:-1] #remove final empty LyricBit
	return lyric_bits

#creates .vectors files for a given .lyric_bits file.
def create_lyric_bits_entities(model, lyrics_bits_filename):
	try:
		lyric_bits = get_lyric_bits(lyrics_bits_filename)
	except:
		print("error with reading the lyric_bits, skipping.")
		return 0
	with open(lyrics_bits_filename + ".vectors", 'w') as vector_file:
		for lyric_bit in lyric_bits:
			lyric_bit.text = clean_lyrics(lyric_bit.text, False)
			vector_file.write("id:" + str(lyric_bit.identifier))
			vector_file.write(printable_vec(create_entity_vector(model, lyric_bit.text.split())))
