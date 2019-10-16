import time
import nltk
import spacy
from spacy.cli.download import download
from helpers import file_helper, time_helper
from modules.parser import Parser
from modules.model import Model
from modules.config import Config
from modules.visualization import Visualization

def main():
    # faz a veirificação da presença de complementos de linguagem necessários ao nltk
    try:
        nltk.tokenize.word_tokenize('Existe nltk punkt')
    except LookupError:
        nltk.download('punkt')

    try:
        spacy.load('pt')
    except IOError:
        download('pt')

    config = Config('data/configuration/', 'config.json')
    # executa as principais funções de cada classe, lendo arquivos de entrada e criando o modelo
    parser = run_data_parse(config)
    model = run_model(config)


    # executa chamadas de predict no modelo
    predict = model.predict()
    dataset_config = config.get_configuration('dataset')
    dataset_path = dataset_config.get('path')
    dataset_test = file_helper.get_json_file_data(dataset_path, dataset_config.get('test_json'))


def run_data_parse(config):
    parse_config = config.get_configuration('parse')
    parser = Parser(config)
    if parse_config.get('parse'):
        parser.run_initial_parse()
    
    return parser


def run_model(config):
    model = Model(config)
    model.create_model()
    model.train_model()
    return model

    

if __name__ == '__main__':
    main()
