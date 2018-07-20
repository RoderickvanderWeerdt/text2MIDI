from w2v_model_generation import generate_w2v_model
from make_midi_subsets import make_lyric_bits
from create_w2v_embeddings_for_lyric_bits import create_w2v_embeddings_for_lyric_bits
from from_midi_to_notesequence import midis_to_notesequence
from musicVAE import remove_wrong_tracks, create_musicVAE_embeddings
from training_mapping import train_mapping
from generate_midi_from_text import generate_midi_from_text

# files:
kaggle_text_file = "input/songdata.csv"
midi_path = "input/midis/"
musicVAE_model_path = "input/MusicVAE_model/mel_16bar_flat/mel_16bar_flat.ckpt"

text_file = "input/text_file.txt"


generate_w2v_model(kaggle_text_file)

make_lyric_bits(midi_path)

create_w2v_embeddings_for_lyric_bits()

midis_to_notesequence()

remove_wrong_tracks(musicVAE_model_path)

midis_to_notesequence()

create_musicVAE_embeddings(musicVAE_model_path)

train_mapping()

generate_midi_from_text(text_file, musicVAE_model_path)