# text2MIDI

This code allows you to create a new piece of MIDI music based on a piece of text. 

The basic idea behind the system is that the lyrics and music of a song both have the same *feeling* (for lack of a better word) that connects them. In order to use this connection between lyrics and music the system creates a vector representation of the lyrics (using Word2Vec) and a vector representation of the music (using the [MusicVAE](https://magenta.tensorflow.org/music-vae) created by Magenta). With a MLP mapping between these two representations the system is able to *translate* a piece of text into a piece of music.

But before you can do that a few files will have to be downloaded and some dependancies installed.
##### Required Packages:
* Magenta
* Keras
* Gensim
* python-midi
* Numpy
* Scipy

##### Required files:
* The w2v model requires a large collection of songlyrics to train. [This collection](https://www.kaggle.com/mousehead/songlyrics) from kaggle has been previously used (and this code has been written with the layout of this collection in mind).
* Fortunately the VAE used has already been trained by Magenta, it can be download [here](http://download.magenta.tensorflow.org/models/music_vae/checkpoints.tar.gz).
* In order to train the mapping between the two models a large set of MIDI files is used.
* Lastly, you will have to create a file with the the text you want your MIDI to be based on.

The paper this code was used for can be found here: LINK TO BE ADDED