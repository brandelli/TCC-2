import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

class Model:

    def __init__(self, params_dict):
        self.params_dict = params_dict
        self.create_model()

    def create_model(self):
        self.model = keras.Sequential([
            # tf.keras.layers.Embedding(tokenizer.vocab_size, 64),
            layers.Embedding(150, 64),
            layers.Bidirectional(layers.LSTM(64)),
            layers.Dense(64, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])

    def train_model(self):
        print('treinando modelo')