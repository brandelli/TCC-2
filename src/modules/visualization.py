import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
class Visualization:

    def __init__(self, config):
        self.config = config


    def get_config(self, str_config=None):
        return self.config.get_configuration(str_config)


    def get_relation_data(self, data):
        relation_dict = {}
        for sentence in data:
            relation = sentence.get('relation')
            if relation_dict.get(relation) is None:
                relation_dict[relation] = 1
            else:
                relation_dict[relation] = relation_dict.get(relation) + 1
        
        return relation_dict

    def get_tuple_relation_data(self, data):
        tuple_dict = {}
        for sentence in data:
            head = sentence.get('head').get('category')
            tail = sentence.get('tail').get('category')
            str_tuple = f'{head}-{tail}'
            if tuple_dict.get(str_tuple) is None:
                tuple_dict[str_tuple] = {'relation': [], 'acc': 0}
            
            tuple_dict[str_tuple].get('relation').append(sentence.get('relation'))
            tuple_dict[str_tuple]['acc'] = tuple_dict[str_tuple].get('acc') + 1 
        
        return tuple_dict
    
    def get_entities_data(self, data):
        entities_dict = {}
        entities_position_list = ['head', 'tail']
        for sentence in data:
            for cur_position in entities_position_list:
                entity = sentence.get(cur_position).get('category')
                if entities_dict.get(entity) is None:
                    entities_dict[entity] = 0
                else:
                    entities_dict[entity] = entities_dict.get(entity) + 1
        
        return entities_dict
    

    def print_predicted_relation(self, dataset, prediction):
        output_file_config = self.get_config('output_files')
        path = output_file_config.get('path')
        file_name = output_file_config.get('debugging')
        with open(f'{path}{file_name}', 'w') as output_file:
            for index, data in enumerate(dataset):
                cur_relation = []
                head = data.get('head').get('word')
                tail = data.get('tail').get('word')
                sentence_id = data.get('sentence_id')
                relation = data.get('relation')
                sentence = data.get('sentence')
                split_sentence = sentence.split(' ')
                pred = prediction[index]
                for i, word in enumerate(split_sentence):
                    if pred[i] == 1:
                        cur_relation.append(word)

                output_file.write(f'========================================\n')
                output_file.write(f'sentence_id: {sentence_id}\n')
                output_file.write(f'sentence: {sentence}\n')
                output_file.write(f'head: {head} | tail: {tail}\n')
                output_file.write(f'expected_relation: {relation}\n')
                output_file.write(f'predicted_relation: {" ".join(cur_relation)}\n')


                print(f'sentence_id: {sentence_id}')
                print(f'sentence_actual_relation: {relation}')
                print(f'sentence_predicted_relation: {" ".join(cur_relation)}')

                
                




    