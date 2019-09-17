import tensorflow as tf

class Model:

    def __init__(self, params_dict):
        self.params_dict = params_dict
        self.create_model()

    def create_model(self):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64))
        ])
        print('Criando modelo')

    def train_model(self):
        print('treinando modelo')