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
    