import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from tensorflow import keras
from helpers import file_helper, data_process_helper
from tensorflow.keras.utils import plot_model

class Model:

    def __init__(self, config):
        self.config = config


    def get_config(self, str_config=None):
        return self.config.get_configuration(str_config)


    def create_model(self):
        # criar funções no helper para processar os dados necessários
        inputs_config = self.get_config('input_for_model')
        outputs_config = self.get_config('output')
        word_embeddings_weight = file_helper.get_json_file_data(inputs_config.get('path'), inputs_config.get('word_embeddings_weight'))
        input_dim, output_dim = data_process_helper.get_embeddings_dimensions(word_embeddings_weight)
        train_input_sentence = file_helper.get_json_file_data(inputs_config.get('path'), inputs_config.get('train_sentence_input'))
        longest_sentence_size = data_process_helper.get_longest_sentence_from_dataset(train_input_sentence)
        output_relations = file_helper.get_json_file_data(outputs_config.get('path'), outputs_config.get('train_relation_output'))
        params_dict = {}
        params_dict['embedding_matrix'] = word_embeddings_weight
        params_dict['input_dim'] = input_dim
        params_dict['output_dim'] = output_dim
        params_dict['train_sentences'] = train_input_sentence
        params_dict['longest_sentence_size'] = longest_sentence_size
        params_dict['output_labels'] = output_relations
        #self.train_model(params_dict)
        positional_input_layer = self.create_input_layer('positional_input_layer', longest_sentence_size)
        word_embeddings_input_layer = self.create_input_layer('word_embeddings_input_layer', longest_sentence_size)


    def create_input_layer(self, str_name, input_length):
        '''
        Cria um layer de input para o modelo
        '''
        return tf.keras.layers.Input(shape=(input_length,), name=str_name)


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
        