import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
class Visualization:

    def get_relation_data(self, data):
        relation_dict = {}
        for sentence in data:
            relation = sentence.get('relation')
            if relation_dict.get(relation) is None:
                relation_dict[relation] = 1
            else:
                relation_dict[relation] = relation_dict[relation] + 1
        
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
        

    