import csv
from helpers import file_helper

class Parser:

    relation_id = 0
    word_id = 1

    def increment_relation_id(self, inc=1):
        self.relation_id += inc

    def increment_word_id(self, inc=1):
        self.word_id += inc

    def tsv_to_json(self, path, file_name, extension='.tsv'):
        '''
        Função para transformar os inputs tabulares em json
        '''
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
            
        file_helper.dict_to_json(path, file_name, input_dict, 4)


    def word_embeddings_to_json(self, path, file_name, extension='.txt'):
        '''
        Função para transformar o arquivo de word_embeddings em json
        '''
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
                
        file_helper.dict_to_json(path, file_name, word_embeddings_list, 4)


    def relation_to_id(self, path, file_name):
        '''
        Função para atribuir um id para cada uma das relações encontradas no dataset de treino
        '''
        treino_json = file_helper.get_json_file_data(path, file_name)
        relation_list = treino_json.get('relation')
        relation_dict = {}
        # primeira relação deve ser NA e o id 0
        relation_dict['NA'] = self.relation_id
        for relation in relation_list:
            if relation_dict.get(relation) is None:
                self.increment_relation_id()
                relation_dict[relation] = self.relation_id
        
        file_helper.dict_to_json('data/relation/', 'relation_2_id', relation_dict, 4)
        
        
