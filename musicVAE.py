import magenta.music as mm
from magenta.music.sequences_lib import concatenate_sequences
from magenta.models.music_vae import configs
from magenta.models.music_vae.trained_model import TrainedModel

from collections import Counter
from os.path import basename, split, join
from os import walk, remove, rmdir

from general_functions import retrieve_dirs

# PATH = "data/training_bits/"

def delete_files_dirs(path, root_path):
	if not path.startswith(root_path):
		print("WATCH OUT!!!")
		return 0
	for root, dirs, files in walk(path, topdown=False):
	    for name in files:
	        remove(join(root, name))
	    for name in dirs:
	        rmdir(join(root, name))
	rmdir(path)

def remove_tracks(relevant_filenames, path, root_path):
	tracks = []
	for rel_filename in relevant_filenames:
		tracks.append(split(rel_filename)[0])
	counted_tracks = Counter(tracks).most_common()

	dirs = retrieve_dirs(path)
	try:
		dirs.remove(split(counted_tracks[0][0])[1])
		for wrong_track in dirs:
			delete_files_dirs(join(root_path, split(counted_tracks[0][0])[0], wrong_track), root_path)
	except:
		print("-- everything will be removed...")
		delete_files_dirs(path, root_path)

	
#delete none relevant filenames
def get_relevent_filenames(model, note_sequences, root_path):
	bit_filenames = model.check_viability(note_sequences)

	dirs = retrieve_dirs(root_path)

	for song_dir in dirs:
		print('--', song_dir)
		relevant_filenames = []
		for bit_filename in bit_filenames:
			if (bit_filename).startswith(song_dir):
				relevant_filenames.append(bit_filename)
		remove_tracks(relevant_filenames, root_path + song_dir, root_path) 

	return relevant_filenames

# # ###works
def encode_note_sequence(model, note_sequences):
	note_sequences, [z, mu, sigma] = model.encode(note_sequences)
	return note_sequences, z

def create_embeddings_for_many(model, note_sequences, root_path):
	rel_filenames, all_z = encode_note_sequence(model, note_sequences)

	i = 1000
	j = 0
	for rel_filename, z in zip(rel_filenames, all_z):
		with open(join(root_path, rel_filename) + '.vector', 'w') as new_file:
			for temp in list(z):
				new_file.write(str(temp)+'\n')
		i -= 1
		if i <= 0:
			j += 1
			i = 1000
			print("handled " + str(j * i) + " vectors.")

def print_sequences(note_sequences):
	print("\nnotesequences in tfrecord:")
	for seq in note_sequences:
		print("--- ", seq.filename)
	print("")

#returns model and NoteSequence. 
def load_model_sequence(model_path, config, note_sequence_file):
	my_model = TrainedModel(config, batch_size=512, checkpoint_dir_or_path=model_path)
	print("loaded the model")

	note_sequences = mm.note_sequence_io.note_sequence_record_iterator(note_sequence_file)
	print("loaded the note_sequence")
	return my_model, note_sequences

#remove all the tracks except for the track with the most 
#encodeable midi parts for every song in the folder.
def remove_wrong_tracks(model_path, config=configs.CONFIG_MAP['flat-mel_16bar'], note_sequence_file="data/notesequence.tfrecord", root_path="data/training_bits/"):
	model, note_sequences = load_model_sequence(model_path, config, note_sequence_file)
	get_relevent_filenames(model, note_sequences, root_path)
	print("removed all the unnecessary tracks.")


def create_musicVAE_embeddings(model_path, config=configs.CONFIG_MAP['flat-mel_16bar'], note_sequence_file="data/notesequence.tfrecord", root_path="data/training_bits/"):
	model, note_sequences = load_model_sequence(model_path, config, note_sequence_file)
	create_embeddings_for_many(model, note_sequences, root_path)
	print("created embeddings for the midi parts.")


### config
# model = "input/MusicVAE_model/mel_16bar_flat/mel_16bar_flat.ckpt"
# my_config = configs.CONFIG_MAP['flat-mel_16bar']
# notesequences = "data/notesequence_selected.tfrecord"
# root_path = "data/training_bits/"

### examples
# rel_filenames = get_relevent_filenames(my_model, note_sequences, root_path) #use to delete!

# create_embeddings_for_many(my_model, note_sequences) #use to create midi embeddings
