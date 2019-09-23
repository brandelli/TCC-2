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

    
    def run_initial_parse(self, config):
        '''
        Função chamada ao iniciar o programa,
        realiza o parse dos arquivos conforme as configurações
        '''
        # chamada para conversão de arquivos originais(txt, tsv) para json
        self.convert_src_to_json_files(config)

        # chamada para criação de dicionários: word_to_id e reverse_dict
        self.create_word_dicts(config)

        # chamada para formatação de inputs que serão utilizados pelo modelo
        self.parse_inputs_for_model(config)

        # chamada para adicionar padding nas sentenças de treino, para que todas tenham o mesmo tamanho
        self.prepare_dataset_for_padding(config)

        # chamada para criar vetores de realcionamentos que vão ser utilizados no input
        self.create_relations_input(config)

    
    def create_relations_input(self, config):
        input_for_model_config = config.get('input_for_model')
        path = input_for_model_config.get('path')
        dataset_config = config.get('dataset')
        train_file_name = input_for_model_config.get('train_relations_input')
        test_file_name = input_for_model_config.get('test_relations_input')
        relations_input_train_data = self.create_individual_relations_input(dataset_config, 'train')
        relations_input_test_data = self.create_individual_relations_input(dataset_config, 'test')
        file_helper.dict_to_json(path, train_file_name, relations_input_train_data, 4)
        file_helper.dict_to_json(path, test_file_name, relations_input_test_data, 4)

    
    def create_individual_relations_input(self, dataset_config, dataset_type):
        relations_list = []
        path = dataset_config.get('path')
        if dataset_type == 'train':
            data = file_helper.get_json_file_data(path, dataset_config.get('train_json'))
        else:
            data = file_helper.get_json_file_data(path, dataset_config.get('test_json'))
        
        for sentence in data:
            entities = []
            entities.append(sentence.get('head').get('id'))
            entities.append(sentence.get('tail').get('id'))
            relations_list.append(entities)
        
        return relations_list

    
    def prepare_dataset_for_padding(self, config):
        input_for_model_config = config.get('input_for_model')
        path = input_for_model_config.get('path')
        file_name = input_for_model_config.get('train_sentence_input')
        input_data = file_helper.get_json_file_data(path, file_name)
        lenght = self.get_longest_sentence_from_dataset(input_data)
        self.include_padding(input_data, lenght)
        file_helper.dict_to_json(path, file_name, input_data, 4)

    
    def include_padding(self, data, padding):
        for sentence in data:
            while len(sentence) < padding:
                sentence.append(0)
    

    def get_longest_sentence_from_dataset(self, data):
        longest = 0
        for sentence in data:
            lenght = len(sentence)
            if lenght > longest:
                longest = lenght
        
        return longest


    def parse_inputs_for_model(self, config):
        '''
        Função para parsear o input de palavras para numeros, tornando melhor para alimentar o modelo
        '''
        word_to_id_config = config.get('word_to_id')
        word_to_id_path = word_to_id_config.get('path')
        word_to_id_file_name = word_to_id_config.get('dict')
        word_to_id = file_helper.get_json_file_data(word_to_id_path, word_to_id_file_name)
        relation_config = config.get('relation')
        relation_path = relation_config.get('path')
        relation_file_name = relation_config.get('file_name')
        relation_dict = file_helper.get_json_file_data(relation_path, relation_file_name)
        self.parse_dataset_for_model(config, 'train', word_to_id, relation_dict)
        self.parse_dataset_for_model(config, 'test', word_to_id, relation_dict)

        # fazer função com logica da criação de matriz de pesos de word embeddings

    
    def parse_dataset_for_model(self, config, dataset_type, word_to_id, relation_dict):
        '''
        Função para iniciar o processo de parseamento dos datasets, para se adequar ao modelo
        '''
        input_for_model_config = config.get('input_for_model')
        dataset_config = config.get('dataset')
        input_for_model_path = input_for_model_config.get('path')
        dataset_path = dataset_config.get('path')
        if dataset_type == 'train':
            input_file_name = input_for_model_config.get('train_sentence_input')
            sentences_dict = file_helper.get_json_file_data(dataset_path, dataset_config.get('train_json'))
            label_file_name = input_for_model_config.get('train_sentence_label')
        else:
            input_file_name = input_for_model_config.get('test_sentence_input')
            sentences_dict = file_helper.get_json_file_data(dataset_path, dataset_config.get('test_json'))
            label_file_name = input_for_model_config.get('test_sentence_label')
        
        parsed_sentence_list, parsed_relation_list = self.parse_sentence_for_model(sentences_dict, word_to_id, relation_dict)
        file_helper.dict_to_json(input_for_model_path, input_file_name, parsed_sentence_list, None)
        file_helper.dict_to_json(input_for_model_path, label_file_name, parsed_relation_list, 4)

    
    def parse_sentence_for_model(self, sentences_dict, word_id, relation_dict):
        '''
        Função para recuperar o valor numérico de relacionamente e palavras presentes nas sentenças
        '''
        parsed_sentence_list = []
        parsed_relation_list = []
        for sentence_dict in sentences_dict:
            words_list = []
            sentence = sentence_dict.get('sentence')
            relation = sentence_dict.get('relation')
            for word in sentence.split(' '):
                words_list.append(word_id.get(word))

            parsed_sentence_list.append(words_list)
            parsed_relation_list.append(relation_dict.get(relation))

        return parsed_sentence_list, parsed_relation_list
    
    def create_word_dicts(self, config):
        '''
        Função que cria os dicionários de palavras(word_to_id, reverse_dict) presentes nos dados de entrada
        '''
        word_to_id_config = config.get('word_to_id')
        path = word_to_id_config.get('path')
        word_to_id_file_name = word_to_id_config.get('dict')
        reverse_dict_file_name = word_to_id_config.get('reverse_dict')
        word_to_id_dict = {}
        reverse_dict = {}
        self.add_word_embeddings_to_word_to_id(config.get('word_embeddings'), word_to_id_dict, reverse_dict)
        self.process_all_dataset_to_word_to_id(config.get('dataset'), word_to_id_dict, reverse_dict)
        file_helper.dict_to_json(path, word_to_id_file_name, word_to_id_dict, 4)
        file_helper.dict_to_json(path, reverse_dict_file_name, reverse_dict, 4)
        
    
    def convert_src_to_json_files(self, config):
        '''
        Função que realiza a conversão dos arquivos de entrada para json
        '''
        parse_config = config.get('parse')

        # transforma o arquivo txt de word embeddings em um json
        if parse_config.get('embeddings'):
            self.word_embeddings_to_json(config.get('word_embeddings'))

        # transforma o arquivo de dataset de treino em json
        if parse_config.get('train'):
            self.dataset_to_json(config.get('dataset'), 'train')
        
        # transforma o arquivo de dataset de test em json
        if parse_config.get('test'):
            self.dataset_to_json(config.get('dataset'), 'test')

        # cria um arquivo json com os relacionamentos presentes no dataset de treino
        if parse_config.get('relation'):
            self.relation_to_id_json(config)


    def dataset_to_json(self, dataset_config, dataset_type):
        '''
        Função para transformar os inputs do dataset em json
        '''
        # vai guardar o index de cada uma das chaves presentes no cabeçalho do arquivo
        keys_dict = {}
        dataset_list = []
        path = dataset_config.get('path')
        if dataset_type == 'train':
            file_name = dataset_config.get('train_tsv')
            json_file_name = dataset_config.get('train_json')
        else:
            file_name = dataset_config.get('test_tsv')
            json_file_name = dataset_config.get('test_json')
        
        with open(f"{path}{file_name}") as fp:
            # faz a leitura do arquivo, utilizando a tabulação como separeador
            reader = csv.reader(fp, delimiter="\t")
            # a primeira linha contém as chaves de cada um dos campos
            keys = reader.__next__()

            # preenche o dicionario de chaves com o indice
            for index, value in enumerate(keys, start=0):
                keys_dict[index] = value.lower()
            
            # para as outras linhas do arquivo vai adicionando cada campo em seu respectivo lugar
            for line in reader:
                cur_dict = dictionary_creator_helper.create_dataset_dict()
                for index, value in enumerate(line):
                    self.process_dataset_data(cur_dict, keys_dict.get(index), value)

                dataset_list.append(cur_dict)
                    
        file_helper.dict_to_json(path, json_file_name, dataset_list, 4)


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


    def word_embeddings_to_json(self, word_embeddings_config):
        '''
        Função para transformar o arquivo de word_embeddings em json
        '''
        # lista de dicionarios com dados processados de word embeddings
        word_embeddings_list = []
        path = word_embeddings_config.get('path')
        # seta o arquivo que vai ser utilizado de word embeddings
        if word_embeddings_config.get('real'):
            file_name = word_embeddings_config.get('real_src')
        else:
            file_name = word_embeddings_config.get('example_src')
  
        with open(f"{path}{file_name}") as fp:
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
                current_word_dict['vec'] = [float(x) for x in data_list]
                word_embeddings_list.append(current_word_dict)
        
        json_file_name = word_embeddings_config.get('word_embeddings_json')
        file_helper.dict_to_json(path, json_file_name, word_embeddings_list, 4)

    def relation_to_id_json(self, config):
        '''
        Função para atribuir um id para cada uma das relações encontradas no dataset de treino
        '''
        dataset_config = config.get('dataset')
        treino_json = file_helper.get_json_file_data(dataset_config.get('path'), dataset_config.get('train_json'))
        relation_config = config.get('relation')
        relation_dict = {}
        # primeira relação deve ser NA e o id 0
        relation_dict['NA'] = self.relation_id
        for line in treino_json:
            relation = line.get('relation')
            if relation_dict.get(relation) is None:
                self.increment_relation_id()
                relation_dict[relation] = self.relation_id
        
        file_helper.dict_to_json(relation_config.get('path'), relation_config.get('file_name'), relation_dict, 4)


    def add_word_to_id(self, word, word_to_id_dict, reverse_dict):
        '''
        Função para adicionar um id para uma palavra
        '''
        if word_to_id_dict.get(word) is None:
            word_to_id_dict[word] = self.word_id
            reverse_dict[self.word_id] = word
            self.increment_word_id()


    def add_word_embeddings_to_word_to_id(self, word_embeddings_config, word_to_id_dict, reverse_dict):
        '''
        Função para atribuir e adicionar ids das palavras encontradas no word embeddings
        '''
        path = word_embeddings_config.get('path')
        file_name = word_embeddings_config.get('word_embeddings_json')
        word_embeddings = file_helper.get_json_file_data(path, file_name)
        for line in word_embeddings:
            self.add_word_to_id(line.get('word'), word_to_id_dict, reverse_dict)
    

    def process_all_dataset_to_word_to_id(self, dataset_config, word_to_id_dict, reverse_dict):
        '''
        Função para iniciar o processamento de todos os datasets (treino, teste)
        para word_to_id
        '''
        path = dataset_config.get('path')
        train_file_name = dataset_config.get('train_json')
        test_file_name = dataset_config.get('test_json')
        self.process_individual_dataset_to_word_to_id(path, train_file_name, word_to_id_dict, reverse_dict)
        self.process_individual_dataset_to_word_to_id(path, test_file_name, word_to_id_dict, reverse_dict)

    
    def process_individual_dataset_to_word_to_id(self, path, file_name, word_to_id_dict, reverse_dict):
        '''
        Função para processar individualmente cada um dos datasets em word_to_id e reverse_dict
        '''
        dict_data = file_helper.get_json_file_data(path, file_name)
        self.add_dataset_to_word_to_id(dict_data, word_to_id_dict, reverse_dict)
        file_helper.dict_to_json(path, file_name, dict_data, 4)
    

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

