from create_w2v_embeddings import create_entity_vectors, create_lyric_bits_entities
from gensim.models import word2vec as w2v

from general_functions import retrieve_lyric_bits_files

def create_w2v_embeddings_for_lyric_bits(model_file="data/w2v_model/lyrics.model", path="data/training_bits"):
	model = w2v.Word2Vec.load(model_file)

	lyric_bits_files = retrieve_lyric_bits_files(path)

	for lyric_bits_file in lyric_bits_files:
		create_lyric_bits_entities(model, lyric_bits_file)

	print("added w2v embeddings to each song.")

### example
# model_file = "data/w2v_model/lyrics.model"
# lyric_bits_location = "training_bits_with_vectors/"
# create_w2v_embeddings_for_lyric_bits(model_file, lyric_bits_location)
