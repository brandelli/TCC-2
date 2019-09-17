import time
from helpers import file_helper, time_helper
from modules.parser import Parser
from modules.model import Model
from modules.config import Config

def main():
    print('Rodando main')
    config = Config('data/configuration/', 'config')
    parser = Parser()
    parser.run_initial_parse(config.get_configuration())
    model = Model(config.get_configuration('model'))

if __name__ == '__main__':
    main()
