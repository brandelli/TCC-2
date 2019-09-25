import tensorflow as tf

class Model:

    def __init__(self, params_dict):
        self.params_dict = params_dict
        self.create_model()

    def create_model(self):
        self.model = tf.keras.Sequential([
            # tf.keras.layers.Embedding(tokenizer.vocab_size, 64),
            tf.keras.layers.Embedding(150, 64),
            tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])

    def train_model(self):
        print('treinando modelo')