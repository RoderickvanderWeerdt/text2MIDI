from process_lyrics import clean_kaggle_songlyrics, clean_txt
from create_w2v_embeddings import create_model, create_entity_vectors, create_test_entity

def generate_w2v_model(text_file, clean_lyrics_file = "data/songlyrics.txt",
						lyrics_index_file = "data/songlyrics.index",
						model_file = "data/w2v_model/lyrics.model",
						make_new_model=True):

	#Model parameters (if a new model is created)
	size = 100
	window = 3
	min_count = 5

	#Main process of the program.

	###MODEL CREATION
	if make_new_model:
		clean_kaggle_songlyrics(text_file, clean_lyrics_file, lyrics_index_file)

	if make_new_model:
		model = create_model(clean_lyrics_file, model_file, make_new_model, size, window, min_count)
	else:
		model = create_model(clean_lyrics_file, model_file, make_new_model)

	print("finished training the w2v model.")

##### example
# generate_w2v_model("input/songdata.csv")