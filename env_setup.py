print 'Importing libraries and defining some helper functions...'
import magenta.music as mm
from magenta.music.sequences_lib import concatenate_sequences
from magenta.models.music_vae import configs
from magenta.models.music_vae.trained_model import TrainedModel
import numpy as np
import os
import tensorflow as tf

def download(note_sequence, filename):
  mm.sequence_proto_to_midi_file(note_sequence, "samples/"+filename)
  #writes to the folder where the code is

print 'Done with Environment Setup'