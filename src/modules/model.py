import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from tensorflow import keras
from helpers import file_helper, data_process_helper
from tensorflow.keras.utils import plot_model

class Model:

    def __init__(self, config):
        self.config = config
        self.model = None
        self.initialize_inputs()
        self.initialize_outputs()
    

    def initialize_inputs(self):
        '''
        Inicializa todos os inputs que vão ser utilizados no modelo
        '''
        inputs_config = self.get_config('input_for_model')
        path = inputs_config.get('path')
        self.word_embeddings_matrix = np.asarray(file_helper.get_json_file_data(path, inputs_config.get('word_embeddings_weight')))
        self.train_positional_input = np.asarray(file_helper.get_json_file_data(path, inputs_config.get('train_positional_vector_input')))
        self.test_positional_input = np.asarray(file_helper.get_json_file_data(path, inputs_config.get('test_positional_vector_input')))
        self.train_sentences = np.asarray(file_helper.get_json_file_data(path, inputs_config.get('train_sentence_input')))
        self.test_sentences = np.asarray(file_helper.get_json_file_data(path, inputs_config.get('test_sentence_input')))
    

    def initialize_outputs(self):
        '''
        Inicializa todos os outputs que vão ser utilizados no modelo
        '''
        outputs_config = self.get_config('output')
        path = outputs_config.get('path')
        self.train_labels = np.asarray(file_helper.get_json_file_data(path, outputs_config.get('train_relation_output')))
        self.test_labels = np.asarray(file_helper.get_json_file_data(path, outputs_config.get('test_relation_output')))


    def get_config(self, str_config=None):
        return self.config.get_configuration(str_config)


    def create_input_layer(self, str_name, input_length):
        '''
        Cria um layer de input para o modelo
        '''
        return tf.keras.layers.Input(shape=(input_length,), name=str_name)

    
    def create_embedding_layer(self, str_name, embedding_matrix, input_length, trainable, model):
        '''
        Cria um layer de embedding para o modelo
        '''
        weights = None if trainable else [embedding_matrix]
        return tf.keras.layers.Embedding(embedding_matrix.shape[0], embedding_matrix.shape[1], weights=weights,input_length=input_length, name=str_name)(model)
    

    def concatenate_layers(self, str_name, layers_list):
        '''
        Concatena uma lista de layers, fazendo merge deles
        '''
        return tf.keras.layers.concatenate(layers_list, name=str_name)


    def create_dense_layer(self, str_name, output_shape, str_activation, model):
        '''
        Cria um layer Dense para o modelo
        '''
        return tf.keras.layers.Dense(output_shape, activation=str_activation, name=str_name)(model)

    
    def create_flatten_layer(self, str_name, model):
        '''
        Cria um layer Flatten para o modelo
        '''
        return tf.keras.layers.Flatten(name=str_name)(model)

    
    def create_bidirectional_layer(self, str_name, lstm, model, merge_mode='concat'):
        '''
        Cria um layer Bidirectional para o modelo
        '''
        return tf.keras.layers.Bidirectional(lstm, merge_mode=merge_mode)(model)

    
    def create_lstm_layer(self, str_name, input_dim, dropout,  bidirectional, model):
        '''
        Cria um layer LSTM para o modelo
        '''
        if bidirectional:
            return tf.keras.layers.LSTM(input_dim, return_sequences=True, dropout=dropout, name=str_name)
        else:
            return tf.keras.layers.LSTM(input_dim, return_sequences=True, dropout=dropout, name=str_name)(model)


    def create_model(self):
        '''
        Cria o modelo que vai ser utilizado, definindo todas as suas camadas e compilação
        '''
        input_length = self.train_sentences.shape[1]
        embeddings_layers = []
        
        # layer de input de posicional de entidades
        positional_input_layer = self.create_input_layer('positional_input_layer', input_length)
        embeddings_layers.append(self.create_embedding_layer('positional_embedding_layer', self.train_positional_input, input_length, True, positional_input_layer))

        # layer de input de word embeddings
        word_embeddings_input_layer = self.create_input_layer('word_embeddings_input_layer', input_length)
        embeddings_layers.append(self.create_embedding_layer('word_embedding_layer', self.word_embeddings_matrix, input_length, True, word_embeddings_input_layer))
        
        # lista com os layers de input
        input_layers = [positional_input_layer, word_embeddings_input_layer]

        # layer para concatenar os embeddings do modelo
        model = self.concatenate_layers('concatenate_embeddings_layer', embeddings_layers)

        # layer LSTM
        lstm = self.create_lstm_layer('lstm_layer', input_length, 0.5, True, model)

        # layer BI-LSTM
        model = self.create_bidirectional_layer('bi_lstm_layer', lstm, model)

        # layer Flatten
        model = self.create_flatten_layer('flatten_layer', model)

        # output layer
        model = self.create_dense_layer('dense_layer_1', 54, 'relu', model)
        model = self.create_dense_layer('dense_layer_2', 54, 'tanh', model)
        
        output = self.create_dense_layer('output_layer', 54, 'softmax', model)

        # criação do modelo
        model = tf.keras.Model(inputs=input_layers, outputs=output)

        # compilação do modelo
        model.compile(loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        print(model.summary())

        self.model = model
        #plot_model(model, to_file='model.png')


    def train_model(self):
        '''
        Realiza o treinamento do modelo
        '''
        train_input_sentence = self.train_sentences
        train_positional_input = self.train_positional_input
        train_output_labels = self.train_labels
        model = self.model
        model.fit([train_positional_input, train_input_sentence], train_output_labels, epochs=40, verbose = 1)
    
    
    def evaluate_model(self):
        model = self.model
        test_sentence_input = self.test_sentences
        test_positional_input = self.test_positional_input
        test_output = self.test_labels
        model.evaluate([test_positional_input, test_sentence_input],test_output)
        