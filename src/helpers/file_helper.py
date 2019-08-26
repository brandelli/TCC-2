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


def word_embeddings_to_json(path, file_name, extension='.txt'):
    '''
    Função para transformar o arquivo de word_embeddings em json
    '''
    print(f"Rodando: {word_embeddings_to_json.__name__}")
    # lista de dicionarios com dados processados de word embeddings
    word_embeddings_list = []
    with open(f"{path}{file_name}{extension}") as fp:
        # primeira linha do arquivo contém o número de linhas e a dimensionalidade do vetor
        lines, vector_size = fp.readline().strip().split(' ')
        lines = int(lines)
        print(f'Número de linhas: {lines}, tamanho do vetor: {vector_size}')
        # itera por todas linhas que contém dados do word embeddings
        for x in range(0 ,lines):
            current_word_dict = {}
            # separa os dados presentes em cada linha, e realiza o pop para separar a word do vetor
            data_list = fp.readline().strip().split(' ')
            word = data_list.pop(0)
            current_word_dict['word'] = word
            # transforma os dados do vetor em float
            current_word_dict['vec'] = list(map(lambda x: float(x), data_list))
            word_embeddings_list.append(current_word_dict)
            
    dict_to_json(path, file_name, word_embeddings_list, 4)
    

def dict_to_json(path, file_name, my_data, indent=0):
    '''
    Função para criar arquivo json com base em dados processados anteriormente
    '''
    with open(f'{path}{file_name}.json', 'w') as json_file:
        json.dump(my_data, json_file, indent=indent)
