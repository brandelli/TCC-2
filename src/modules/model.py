import tensorflow as tf
from tensorflow import keras
from helpers import file_helper, data_process_helper
import numpy as np

class Model:

    def __init__(self, config):
        self.config = config


    def get_config(self, str_config=None):
        return self.config.get_configuration(str_config)


    def start_model_creation(self):
        # criar funções no helper para processar os dados necessários
        inputs_config = self.get_config('input_for_model')
        outputs_config = self.get_config('output')
        word_embeddings_weight = file_helper.get_json_file_data(inputs_config.get('path'), inputs_config.get('word_embeddings_weight'))
        input_dim, output_dim = data_process_helper.get_embeddings_dimensions(word_embeddings_weight)
        train_input_sentence = file_helper.get_json_file_data(inputs_config.get('path'), inputs_config.get('train_sentence_input'))
        longest_sentence_size = data_process_helper.get_longest_sentence_from_dataset(train_input_sentence)
        output_relations = file_helper.get_json_file_data(outputs_config.get('path'), outputs_config.get('train_relation_output'))
        print('word embeddings')
        print(f'input_dim: {input_dim} | output_dim: {output_dim}')
        print('train sentences input')
        print(train_input_sentence)
        print(f'longest_sentence_size: {longest_sentence_size}')
        params_dict = {}
        params_dict['embedding_matrix'] = word_embeddings_weight
        params_dict['input_dim'] = input_dim
        params_dict['output_dim'] = output_dim
        params_dict['train_sentences'] = train_input_sentence
        params_dict['longest_sentence_size'] = longest_sentence_size
        params_dict['output_labels'] = output_relations
        self.train_model(params_dict)



        

    def train_model(self, params_dict):
        embedding_matrix = params_dict.get('embedding_matrix')
        input_dim = params_dict.get('input_dim')
        output_dim = params_dict.get('output_dim')
        sentences_lenght = params_dict.get('longest_sentence_size')
        train_input_sentence = params_dict.get('train_sentences')
        output_labels = params_dict.get('output_labels')
        input = tf.keras.layers.Input(shape=(sentences_lenght,))
        model = tf.keras.layers.Embedding(input_dim,output_dim,weights=np.array([embedding_matrix]),input_length=sentences_lenght)(input)
        model =  tf.keras.layers.Bidirectional(tf.keras.layers.LSTM (input_dim,return_sequences=True,dropout=0.2),merge_mode='concat')(model)
        model = tf.keras.layers.Flatten()(model)
        output = tf.keras.layers.Dense(54,activation='softmax')(model)
        model = tf.keras.Model(input,output)
        model.compile(loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        model.fit(train_input_sentence,output_labels, epochs=30, verbose = 1)
        print(model.summary())
        prediction_probas = model.predict(train_input_sentence)
        predictions = [np.argmax(pred) for pred in prediction_probas]
        print(predictions)
        for index in range(len(output_labels)):
            print(f'expected: {output_labels[index]} | predicted: {predictions[index]}')

        
        loss, accuracy = model.evaluate(train_input_sentence, output_labels, verbose=1)
        print(f'loss: {loss} | accuracy: {accuracy}')
        