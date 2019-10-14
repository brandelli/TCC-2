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
    run_data_parse(config)
    #run_data_visualization(config)
    run_model(config)


def run_data_parse(config):
    parse_config = config.get_configuration('parse')
    if parse_config.get('parse'):
        parser = Parser(config)
        parser.run_initial_parse()


def run_data_visualization(config):
    visualization = Visualization()
    dataset_config = config.get_configuration('dataset')
    dataset_path = dataset_config.get('path')
    dataset_train = file_helper.get_json_file_data(dataset_path, dataset_config.get('train_json'))
    dataset_test = file_helper.get_json_file_data(dataset_path, dataset_config.get('test_json'))
    output_config = config.get_configuration('output')
    output_path = output_config.get('path')
    output_train = file_helper.get_json_file_data(output_path, output_config.get('train_sentence_output'))
    output_test = file_helper.get_json_file_data(output_path, output_config.get('test_sentence_output'))
    print('=================visualizando output de treino================================')
    visualization.print_predicted_relation(dataset_train, output_train)
    print('=================visualizando output de teste=================================')
    visualization.print_predicted_relation(dataset_test, output_test)


def run_model(config):
    model = Model(config)
    model.create_model()
    model.train_model()
    predict = model.predict()
    visualization = Visualization()
    dataset_config = config.get_configuration('dataset')
    dataset_path = dataset_config.get('path')
    dataset_test = file_helper.get_json_file_data(dataset_path, dataset_config.get('test_json'))

    visualization.print_predicted_relation(dataset_test, predict)

    

if __name__ == '__main__':
    main()
