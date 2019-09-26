import time
import nltk
from helpers import file_helper, time_helper
from modules.parser import Parser
from modules.model import Model
from modules.config import Config

def main():
    # faz a veirificação da presença de complementos de linguagem necessários ao nltk
    try:
        nltk.tokenize.word_tokenize('Existe nltk punkt')
    except LookupError:
        nltk.download('punkt')

    print('Rodando main')
    config = Config('data/configuration/', 'config.json')
    parser = Parser(config)
    parser.run_initial_parse()
    model = Model(config.get_configuration('model'))

if __name__ == '__main__':
    main()
