#based on "Multilayer Perceptron (MLP) for multi-class softmax classification" from https://keras.io/getting-started/sequential-model-guide/

from create_vector_pairs import get_training_data
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD

# Generate dummy data
import numpy as np

def save_model(model, model_name):
	with open("data/mapping_model/" + model_name + ".json", 'w') as model_file:
		json_string = model.to_json()
		model_file.write(json_string)
	model.save_weights("data/mapping_model/" + model_name + ".hdf5")

def create_model():
	model = Sequential()
	model.add(Dense(256, activation='relu', input_dim=100))
	model.add(Dense(1024, activation='relu'))
	model.add(Dense(512, activation='linear'))

	sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
	model.compile(loss='mean_squared_error', optimizer=sgd)
	return model

def train_mapping(path="data/training_bits/"):
	x, y = get_training_data(path)

	test_size = int(np.floor(len(x) * 0.1))
	# test_size = len(x) - 50

	print("training/validation set = ", len(x) - test_size, "\nevaluation set = ", test_size)

	x_test = np.array(x[:test_size])
	x_train = np.array(x[test_size:])
	y_test = np.array(y[:test_size])
	y_train = np.array(y[test_size:])

	print(len(x_test))

	model = create_model()

	model.fit(x_train, y_train,
						epochs=120,
						batch_size=512,
						validation_split=0.1)

	print("starting evaluation...")
	score = model.evaluate(x_test, y_test, batch_size=512)

	print("final score =", score)
	print("")

	print("saving model...")
	save_model(model, "mapping_model_with_melody_instruments")
	print("the mapping model has been saved.")

### example
# train_mapping("data/training_bits/")


