import csv
from helpers import file_helper

class Parser:

    relation_id = 0
    word_id = 1

    def increment_relation_id(self, inc=1):
        self.relation_id += inc


    def increment_word_id(self, inc=1):
        self.word_id += inc

    
    def dataset_to_json(self, path, file_name, extension='.tsv'):
        '''
        Função para transformar os inputs tabulares em json
        '''
        # vai guardar o index de cada uma das chaves presentes no cabeçalho do arquivo
        keys_dict = {}
        dataset_list = []
        with open(f"{path}{file_name}{extension}") as tsvfile:
            # faz a leitura do arquivo, utilizando a tabulação como separeador
            tsvreader = csv.reader(tsvfile, delimiter="\t")
            # a primeira linha contém as chaves de cada um dos campos
            keys = tsvreader.__next__()

            # preenche o dicionario de chaves com o indice
            for index, value in enumerate(keys, start=0):
                keys_dict[index] = value.lower()
            
            # para as outras linhas do arquivo vai adicionando cada campo em seu respectivo lugar
            for line in tsvreader:
                cur_dict = self.create_dataset_dict()
                cur_dict = {}
                for index, value in enumerate(line):
                    self.process_dataset_data(cur_dict, keys_dict.get(index), value)
                dataset_list.append(cur_dict)
                    
        file_helper.dict_to_json(path, file_name, dataset_list, 4)

    
    def create_dataset_dict(self):
        return {
            'sentence_id': None,
            'sentence': None,
            'head': {
                'word': None,
                'id': None,
                'category': None
            },
            'tail': {
                'word': None,
                'id': None,
                'category': None
            },
            'relation': None,
            'relation_id': None
        }


    def process_dataset_data(self, cur_dict, key, value):
        cur_dict[key] = value
        # lógica para verificação de qual key está sendo recebida

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
            for _ in range(0 ,lines):
                current_word_dict = {}
                # separa os dados presentes em cada linha, e realiza o pop para separar a word do vetor
                data_list = fp.readline().strip().split(' ')
                word = data_list.pop(0)
                current_word_dict['word'] = word
                # transforma os dados do vetor em float
                current_word_dict['vec'] = list(map(lambda x: float(x), data_list))
                word_embeddings_list.append(current_word_dict)
                
        file_helper.dict_to_json(path, file_name, word_embeddings_list, 4)

    # vai ter que mudar essa função
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
        
        
