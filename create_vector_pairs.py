from general_functions import retrieve_vector_files, retrieve_vectors_files

from os.path import basename

from numpy import array

class Vector_Pair:
	# def __init__(self, name, part_id, midi_vector = [], text_vector = []):
	def __init__(self, midi_vector, text_vector = []):
		# self.song_name = name
		# self.part_id = part_id
		self.midi_vector = midi_vector
		self.text_vector = text_vector

# def make_list_of

def get_song_folder(path, path_to):
	return path[len(path_to):path.find('/', len(path_to))]


def retrieve_midi_vectors(midi_vectors, path):
	vector_pairs_dict = {}
	for midi_vector in midi_vectors:
		with open(midi_vector, 'r') as vector:
			part_id = basename(midi_vector[midi_vector.lower().find(".mid")+4:])[:-11] #remove PATH, songname, ".mid.vector" to leave the id of the song_part
			song_name = get_song_folder(midi_vector, path)

			new_vector = []
			for n in vector.readlines(): new_vector.append(float(n[:-1]))

			# vector_pair = Vector_Pair(song_name, part_id, new_vector)
			vector_pair = Vector_Pair(new_vector)

			try:
				vector_pairs_dict[song_name][part_id] = vector_pair
			except:
				vector_pairs_dict[song_name] = {}
				vector_pairs_dict[song_name][part_id] = vector_pair
	return vector_pairs_dict

def retrieve_text_vectors(text_vectors, vector_pairs_dict, path):
	for text_vector in text_vectors:
		song_name = get_song_folder(text_vector, path)
		# lyric_bit_dict = {}
		dict_pointer = 0
		with open(text_vector, 'r') as vectors:
			for line in vectors.readlines():
				if line.startswith('id:'):
					part_id = line[3:-1] #remove "id:" and "\n"
					dict_pointer = part_id
				else:
					# lyric_bit_dict[dict_pointer] = list(line[:-1].split(','))
					try:
						new_vector = []
						for x in list(line[:-1].split(',')): new_vector.append(float(x))
						vector_pairs_dict[song_name][dict_pointer].text_vector = new_vector
					except:
						# print("this text vector does not have a corresponding midi vector.")
						pass

	return vector_pairs_dict

def create_vector_pairs_dict(path):
	text_vectors = retrieve_vectors_files(path)
	midi_vectors = retrieve_vector_files(path)

	vector_pairs_dict_without_text = retrieve_midi_vectors(midi_vectors, path)

	return retrieve_text_vectors(text_vectors, vector_pairs_dict_without_text, path)

def get_training_data(path):
	vector_pairs_dict = create_vector_pairs_dict(path)

	x = []
	y = []
	for vector_pair_songname in vector_pairs_dict.keys():
		# print("handling song: " + vector_pair_songname)
		for vector_pair_song_part in vector_pairs_dict[vector_pair_songname].keys():
			vector_pair = vector_pairs_dict[vector_pair_songname][vector_pair_song_part]
			if len(vector_pair.text_vector) == 100 and len(vector_pair.midi_vector) == 512:
				x.append(vector_pair.text_vector)
				y.append(vector_pair.midi_vector)

	return x, y

# x, y = get_training_data()
