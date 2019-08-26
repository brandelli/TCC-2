import csv
import json

def tsv_to_json(path, file_name, extension='.tsv'):
    '''
    Função para transformar os inputs tabulares em json
    '''
    print(f"Rodando: {tsv_to_json.__name__}")
    # vai guardar o index de cada uma das chaves presentes no cabeçalho do arquivo
    keys_dict = {}
    input_dict = {}
    with open(f"{path}{file_name}{extension}") as tsvfile:
        # faz a leitura do arquivo, utilizando a tabulação como separeador
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        # a primeira linha contém as chaves de cada um dos campos
        keys = tsvreader.__next__()

        # preenche o dicionario de chaves com o indice
        for index, value in enumerate(keys, start=0):
            keys_dict[index] = value.lower()
            input_dict[value.lower()] = []
        
        # para as outras linhas do arquivo vai adicionando cada campo em seu respectivo lugar
        for line in tsvreader:
            for index, value in enumerate(line):
                input_dict[keys_dict.get(index)].append(value)
        
    dict_to_json(path, file_name, input_dict, 4)
    

def dict_to_json(path, file_name, my_dict, indent=0):
    with open(f'{path}{file_name}.json', 'w') as json_file:
        json.dump(my_dict, json_file, indent=indent)
