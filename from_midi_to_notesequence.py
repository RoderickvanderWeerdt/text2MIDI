from magenta.scripts.convert_dir_to_note_sequences import convert_directory

def midis_to_notesequence(midi_folder="data/training_bits", notesequence_file="data/notesequence.tfrecord"):
	convert_directory(midi_folder, notesequence_file, True)
	print("created a new notesequence.")

##### example
# midis_to_notesequence("input/midis", "data/notesequences.tf")