import csv
from helpers import file_helper, validator_helper, data_process_helper, dictionary_creator_helper

class Parser:

    relation_id = 0
    word_id = 1

    def increment_relation_id(self, inc=1):
        '''
        Função para incrementar o relation_id
        '''
        self.relation_id += inc


    def increment_word_id(self, inc=1):
        '''
        Função para incrementar o word_id
        '''
        self.word_id += inc

    
    def dataset_to_json(self, path, file_name, extension='.tsv'):
        '''
        Função para transformar os inputs do dataset em json
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
                cur_dict = dictionary_creator_helper.create_dataset_dict()
                for index, value in enumerate(line):
                    self.process_dataset_data(cur_dict, keys_dict.get(index), value)

                dataset_list.append(cur_dict)
                    
        file_helper.dict_to_json(path, file_name, dataset_list, 4)


    def process_dataset_data(self, cur_dict, key, value):
        '''
        Função para processar os dados do dataset de acordo com os campos
        '''
        if validator_helper.is_id_data(key):
            data_process_helper.process_id_data(cur_dict, key, value)
        elif validator_helper.is_entity(key):
            data_process_helper.process_entity_data(cur_dict, key, value)
        elif validator_helper.is_category(key):
            data_process_helper.process_category_data(cur_dict, key, value)
        elif validator_helper.is_sentence(key):
            data_process_helper.process_sentence_data(cur_dict, key, value)
        elif validator_helper.is_relation(key):
            data_process_helper.process_relation_data(cur_dict, key, value)


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

    def relation_to_id(self, path, file_name):
        '''
        Função para atribuir um id para cada uma das relações encontradas no dataset de treino
        '''
        treino_json = file_helper.get_json_file_data(path, file_name)
        relation_dict = {}
        # primeira relação deve ser NA e o id 0
        relation_dict['NA'] = self.relation_id
        for line in treino_json:
            relation = line.get('relation')
            if relation_dict.get(relation) is None:
                self.increment_relation_id()
                relation_dict[relation] = self.relation_id
        
        file_helper.dict_to_json('data/relation/', 'relation_2_id', relation_dict, 4)

    def create_word_to_id(self):
        '''
        Função para criar a estrutura de word_to_id
        '''
        word_to_id_dict = {}
        reverse_dict = {}
        path = 'data/word_to_id/'
        self.add_word_embeddings_to_word_to_id(word_to_id_dict, reverse_dict)
        self.process_dataset_to_word_to_id(word_to_id_dict, reverse_dict)
        file_helper.dict_to_json(path, 'word_to_id', word_to_id_dict, 4)
        file_helper.dict_to_json(path, 'reverse_dict', reverse_dict, 4)

    def add_word_to_id(self, word, word_to_id_dict, reverse_dict):
        '''
        Função para adicionar um id para uma palavra
        '''
        if word_to_id_dict.get(word) is None:
            word_to_id_dict[word] = self.word_id
            reverse_dict[self.word_id] = word
            self.increment_word_id()

    def add_word_embeddings_to_word_to_id(self, word_to_id_dict, reverse_dict):
        '''
        Função para atribuir e adicionar ids das palavras encontradas no word embeddings
        '''
        word_embeddings = file_helper.get_json_file_data('data/word_embeddings/exemplo/', 'word_embeddings')
        for line in word_embeddings:
            self.add_word_to_id(line.get('word'), word_to_id_dict, reverse_dict)
        
    def process_dataset_to_word_to_id(self, word_to_id_dict, reverse_dict):
        '''
        Função para iniciar o processamento de todos os datasets (treino, teste)
        para word_to_id
        '''
        path = 'data/dataset/'
        treino = file_helper.get_json_file_data(path, 'treino')
        self.add_dataset_to_word_to_id(treino, word_to_id_dict, reverse_dict)
        file_helper.dict_to_json(path, 'treino', treino, 4)
        teste = file_helper.get_json_file_data(path, 'teste_1')
        self.add_dataset_to_word_to_id(teste, word_to_id_dict, reverse_dict)
        file_helper.dict_to_json(path, 'teste_1', teste, 4)
    
    def add_dataset_to_word_to_id(self, dataset, word_to_id_dict, reverse_dict):
        '''
        Função para transformar todas palavras das frases presentes 
        no dataset em word_to_id
        '''
        for line in dataset:
            sentence = line.get('sentence')
            for word in sentence.split(' '):
                self.add_word_to_id(word, word_to_id_dict, reverse_dict)
            
            self.set_word_id_to_entity_in_dataset(line, word_to_id_dict)
    
    def set_word_id_to_entity_in_dataset(self, dataset_line, word_to_id_dict):
        head = dataset_line.get('head')
        tail = dataset_line.get('tail')
        head['id'] = word_to_id_dict.get(head.get('word'))
        tail['id'] = word_to_id_dict.get(tail.get('word'))