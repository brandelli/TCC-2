import time
import nltk
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
        nltk.pos_tag(nltk.word_tokenize('Existe nltk averaged_perceptron_tagger'))
    except LookupError:
        nltk.download('averaged_perceptron_tagger')

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
    visualization.get_relation_data(dataset_train)
    visualization.get_tuple_relation_data(dataset_train)
    print(visualization.get_entities_data(dataset_train))


def run_model(config):
    model = Model(config)
    model.create_model()
    model.train_model()
    model.evaluate_model()
    predict = model.predict()
    

if __name__ == '__main__':
    main()
