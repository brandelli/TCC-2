import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from tensorflow import keras
from helpers import file_helper, data_process_helper
from tensorflow.keras.utils import plot_model

class Model:

    def __init__(self, config):
        self.config = config
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
        self.train_sentences = np.asarray(file_helper.get_json_file_data(path, inputs_config.get('train_sentence_input')))
    

    def initialize_outputs(self):
        '''
        Inicializa todos os outputs que vão ser utilizados no modelo
        '''
        outputs_config = self.get_config('output')
        path = outputs_config.get('path')
        self.train_labels = np.asarray(file_helper.get_json_file_data(path, outputs_config.get('train_relation_output')))


    def get_config(self, str_config=None):
        return self.config.get_configuration(str_config)


    def create_model(self):
        # criar funções no helper para processar os dados necessários
        #self.train_model(params_dict)
        #positional_input_layer = self.create_input_layer('positional_input_layer', longest_sentence_size)
        #word_embeddings_input_layer = self.create_input_layer('word_embeddings_input_layer', longest_sentence_size)


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
        return tf.keras.layers.Embedding(embedding_matrix.shape[0], embedding_matrix.shape[1], weights=[weights],input_length=input_length, name=str_name)(model)
    

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

    
    def create_bidirectional_layer(self, str_name, model, merge_mode='concat'):
        '''
        Cria um layer Bidirectional para o modelo
        '''
        return tf.keras.layers.Bidirectional(model, merge_mode=merge_mode)

    
    def create_lstm_layer(self, str_name, input_dim, dropout,  bidirectional, model):
        '''
        Cria um layer LSTM para o modelo
        '''
        if bidirectional:
            return tf.keras.layers.LSTM(input_dim, return_sequences=True, dropout=dropout, name=str_name)
        else:
            return tf.keras.layers.LSTM(input_dim, return_sequences=True, dropout=dropout, name=str_name)(model)


    def train_model(self, params_dict):
        embedding_matrix = np.asarray(params_dict.get('embedding_matrix'))
        input_dim = params_dict.get('input_dim')
        output_dim = params_dict.get('output_dim')
        sentences_lenght = params_dict.get('longest_sentence_size')
        train_input_sentence = np.asarray(params_dict.get('train_sentences'))
        output_labels = np.asarray(params_dict.get('output_labels'))
        position_vector = np.asarray(params_dict['train_positional_vector_input'])

        # input do vetor posicional
        position_vector_input = tf.keras.layers.Input(shape=(sentences_lenght,))
        embed_position_vector = tf.keras.layers.Embedding(input_dim,output_dim,input_length=sentences_lenght)(position_vector_input)

        # input da sentença, que passa junto ao word embedding
        word_embeddings_input = tf.keras.layers.Input(shape=(sentences_lenght,))
        embed_word_embeddings = tf.keras.layers.Embedding(input_dim,output_dim,weights=[embedding_matrix],input_length=sentences_lenght)(word_embeddings_input)

        # concatendo os dois embeddings
        model = tf.keras.layers.concatenate([embed_word_embeddings, embed_position_vector])

        # camada de LSTM
        model = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM (input_dim,return_sequences=True,dropout=0.5),merge_mode='concat')(model)

        # algumas camadas extras
        model = tf.keras.layers.Flatten()(model)
        output = tf.keras.layers.Dense(54,activation='softmax')(model)
        model = tf.keras.Model(inputs=[word_embeddings_input, position_vector_input],outputs=output)
        model.compile(loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        print(model.summary())
        history = model.fit([train_input_sentence, position_vector], output_labels, epochs=40, verbose = 1)
        plt.plot(history.history['accuracy'])
        plt.title('Model accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend(['Train'], loc='upper left')
        plt.show()
        
        prediction_probas = model.predict([train_input_sentence, position_vector])
        predictions = [np.argmax(pred) for pred in prediction_probas]
        print(predictions)
        for index in range(len(output_labels)):
            print(f'expected: {output_labels[index]} | predicted: {predictions[index]}')

        
        loss, accuracy = model.evaluate([train_input_sentence, position_vector], output_labels, verbose=1)
        print(f'loss: {loss} | accuracy: {accuracy}')
        