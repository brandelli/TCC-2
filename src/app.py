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


    config = Config('data/configuration/', 'config.json')
    parse_config = config.get_configuration('parse')
    if parse_config.get('parse'):
        parser = Parser(config)
        parser.run_initial_parse()

    model = Model(config)

    visualization = Visualization()
    visualization.teste()
    #model.start_model_creation()

if __name__ == '__main__':
    main()
