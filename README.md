# text2MIDI

This code allows you to create a new piece of MIDI music based on a piece of text. 

The basic idea behind the system is that the lyrics and music of a song both have the same *feeling* (for lack of a better word) that connects them. In order to use this connection between lyrics and music the system creates a vector representation of the lyrics (using Word2Vec) and a vector representation of the music (using the [MusicVAE](https://magenta.tensorflow.org/music-vae) created by Magenta). With a MLP mapping between these two representations the system is able to *translate* a piece of text into a piece of music.

But before you can do that a few files will have to be downloaded, some dependancies installed and one file will have to be altered.

#### Guide
1) Make sure you are running Python 2.7, if not set up an environment which does.
2) Install the required packages with the requirements file and pip.
3) Download all the required files:
    * The w2v model requires a large collection of songlyrics to train. [This collection](https://www.kaggle.com/mousehead/songlyrics) from kaggle has been previously used (and this code has been written with the layout of this collection in mind). The songlyrics should be saved in `input/songdata.csv`.
    * Fortunately the VAE used has already been trained by Magenta, it can be download [here](http://download.magenta.tensorflow.org/models/music_vae/checkpoints.tar.gz). The mel_16bar_flat model should be saved here: `input/MusicVAE_model/mel_16bar_flat/`.
    * In order to train the mapping between the two models a large set of MIDI files is needed, it must be stored in the folder `input/midis/`.
4) Some changes are required in the `trained_model.py` file in your magenta package, the changed file is available in this repository, but it will still have to be replaced in the magenta package folder. If you are using anaconda for your environment it usually can be found here: `<hard-drive>/anaconda3/envs/<env-name>/lib/python2.7/site-packages/magenta/models/music_vae/trained_model.py`
99) Lastly, you will have to create a file with the the text you want your MIDI to be based on, and save it in `/input/textfile.txt`

When all steps have been performed the program can be started by running `main-pipeline.py` from the terminal.
