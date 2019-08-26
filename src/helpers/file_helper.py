import json

def dict_to_json(path, file_name, my_data, indent=0):
    '''
    Função para criar arquivo json com base em dados processados anteriormente
    '''
    with open(f'{path}{file_name}.json', 'w') as json_file:
        json.dump(my_data, json_file, indent=indent)


def get_json_file_data(path, file_name):
    json_data = {}    
    with open(f'{path}{file_name}.json') as json_file:
        json_data = json.load(json_file)
    
    return json_data
