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
        inputs_config = self.get_config('input')
        path = inputs_config.get('path')

        # word embeddings pesos já treinados
        self.word_embeddings_matrix = np.asarray(file_helper.get_json_file_data(path, inputs_config.get('word_embeddings_weight')))
        '''
        print('word_embeddings_matrix')
        print(self.word_embeddings_matrix)
        '''

        # inputs de treino
        self.train_sentences_input = np.asarray(file_helper.get_json_file_data(path, inputs_config.get('train_sentence_input')))
        self.train_entities_input = np.asarray(file_helper.get_json_file_data(path, inputs_config.get('train_entity_input')))
        '''
        print('train_sentences_input')
        print(self.train_sentences_input)
        print('train_entities_input')
        print(self.train_entities_input)
        '''

        # inputs de teste
        self.test_sentences_input = np.asarray(file_helper.get_json_file_data(path, inputs_config.get('test_sentence_input')))
        self.test_entities_input = np.asarray(file_helper.get_json_file_data(path, inputs_config.get('test_entity_input')))
        '''
        print('test_sentences_input')
        print(self.test_sentences_input)
        print('test_entities_input')
        print(self.test_entities_input)
        '''
    

    def initialize_outputs(self):
        '''
        Inicializa todos os outputs que vão ser utilizados no modelo
        '''
        outputs_config = self.get_config('output')
        path = outputs_config.get('path')

        # output de treino
        self.train_sentences_output = np.asarray(file_helper.get_json_file_data(path, outputs_config.get('train_sentence_output')))
        '''
        print('train_sentences_output')
        print(self.train_sentences_output)
        '''

        # output de teste
        self.test_sentences_output = np.asarray(file_helper.get_json_file_data(path, outputs_config.get('test_sentence_output')))
        '''
        print('test_sentences_output')
        print(self.test_sentences_output)
        '''


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
    

    def create_time_distributed(self, str_name, output_dim, str_activation, model):
        '''
        Cria um layer Time Distributed para o modelo
        '''
        return tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(output_dim, activation=str_activation), name=str_name)(model)


    def create_model(self):
        '''
        Cria o modelo que vai ser utilizado, definindo todas as suas camadas e compilação
        '''
        input_length = self.train_sentences_input.shape[1]
        embeddings_layers = []
        input_layers = []
        
        # layer de input de word embeddings
        word_embeddings_input_layer = self.create_input_layer('word_embeddings_input_layer', input_length)
        input_layers.append(word_embeddings_input_layer)
        embeddings_layers.append(self.create_embedding_layer('word_embedding_layer', self.word_embeddings_matrix, input_length, False, word_embeddings_input_layer))

        # layer de input de entidades
        entity_input_layer = self.create_input_layer('entity_input_layer', input_length)
        input_layers.append(entity_input_layer)
        embeddings_layers.append(self.create_embedding_layer('entity_embedding_layer', self.train_entities_input, input_length, True, entity_input_layer))
        
        print(input_layers)

        # layer para concatenar os embeddings do modelo
        model = self.concatenate_layers('concatenate_embeddings_layer', embeddings_layers)

        # layer LSTM
        lstm = self.create_lstm_layer('lstm_layer', input_length, 0.2, True, model)

        # layer BI-LSTM
        model = self.create_bidirectional_layer('bi_lstm_layer', lstm, model)

        # layer Flatten
        #model = self.create_flatten_layer('flatten_layer_1', model)

        model = self.create_dense_layer('dense_layer_1', 64, 'tanh', model)
        model = self.create_dense_layer('dense_layer_2', 64, 'relu', model)

        output = self.create_time_distributed('time_distributed_layer', 2, 'softmax', model)

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
        train_inputs = [self.train_sentences_input, self.train_entities_input]
        train_sentences_output = self.train_sentences_output
        model = self.model
        model.fit(train_inputs, train_sentences_output, epochs=30, verbose = 1)
    
    
    def evaluate_model(self):
        model = self.model
        test_sentence_input = self.test_sentences
        test_positional_input = self.test_positional_input
        test_e1_relative_input = self.test_e1_relative
        test_e2_relative_input = self.test_e2_relative
        test_output = self.test_labels
        train_input_sentence = self.train_sentences
        train_positional_input = self.train_positional_input
        train_e1_relative_input = self.train_e1_relative
        train_e2_relative_input = self.train_e2_relative
        train_output_labels = self.train_labels
        #model.evaluate([train_positional_input, train_input_sentence],train_output_labels)
        #model.evaluate([test_positional_input, test_sentence_input],test_output)
        