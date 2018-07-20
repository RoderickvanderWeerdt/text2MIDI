from create_w2v_embeddings import create_test_entities, create_single_entity

from mapping_z import make_mapping

# from MusicVAE import decode_vectors
from magenta.music.sequences_lib import concatenate_sequences
from magenta.models.music_vae.trained_model import TrainedModel
from magenta.models.music_vae import configs

import magenta.music as mm

def download(note_sequence, filename):
	mm.sequence_proto_to_midi_file(note_sequence, "output/"+filename)
	#writes to the folder where the code is

def decode_vectors(model_file, vectors, concatenate=False):
	temperature = 1.0 #param: min:0.1, max:1.5
	config = configs.CONFIG_MAP['flat-mel_16bar']
	model = TrainedModel(config, batch_size=512, checkpoint_dir_or_path=model_file)
	resulting_midis = model.decode(vectors, length=256)
	if concatenate:
		concatenated_midis = concatenate_sequences(resulting_midis)
		download(concatenated_midis, "concatenated_midi.mid")
		print("created 1 midi.")
	else:
		for i, p in enumerate(resulting_midis):
			download(p, "newly_created_"+str(i)+".mid")
			print("created " + str(len(resulting_midis)) + " midis")

def generate_midi_from_text(text_file, musicvae_model_path,
							w2v_model_file="data/w2v_model/lyrics.model", 
							mapping_model_file="data/mapping_model/mapping_model_with_melody_instruments.json", 
							mapping_weights_file="data/mapping_model/mapping_model_with_melody_instruments.hdf5"):
	#encode text to w2v vector
	w2v_vectors = create_single_entity(w2v_model_file, text_file) #creates one vector

	#make mapping
	midi_vectors = make_mapping(mapping_model_file, mapping_weights_file, w2v_vectors)

	# decode midi from midi_vectors
	decode_vectors(musicvae_model_path, midi_vectors, concatenate=False)

### example
# #models
# w2v_model_file = "data/w2v_model/lyrics.model"
# mapping_model_file = "data/mapping_model/mapping_model_with_melody_instruments.json"
# mapping_weights_file = "data/mapping_model/mapping_model_with_melody_instruments.hdf5"
# musicvae_model_file = "input/MusicVAE_model/mel_16bar_flat/mel_16bar_flat.ckpt"
# generate_midi_from_text("input/text_file", musicvae_model_file, w2v_model_file, mapping_model_file, mapping_weights_file)