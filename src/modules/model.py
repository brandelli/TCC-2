import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import Model
from tensorflow.keras import Input
from helpers import file_helper

class Model:

    def __init__(self, config):
        self.config = config


    def get_config(self, str_config=None):
        return self.config.get_configuration(str_config)


    def start_model_creation(self):
        # criar funções no helper para processar os dados necessários
        inputs_config = self.get_config('input_for_model')
        word_embeddings_weight = file_helper.get_json_file_data(inputs_config.get('path'), inputs_config.get('word_embeddings_weight'))
        print(f'input_dim:{len(word_embeddings_weight)} | output_dim: {len(word_embeddings_weight[0])}')
        

    def train_model(self):
        print('treinando modelo')