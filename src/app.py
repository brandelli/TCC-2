import time
from helpers import file_helper, time_helper
from modules.parser import Parser
from modules.model import Model
from modules.config import Config

def main():
    start = time.time()
    elapsed_time = lambda start_time: time_helper.get_elapsed_time(start_time)
    print_elapsed_time = lambda process, start_time: print(f'Finalizou {process} {elapsed_time(start_time)}')
    get_time = lambda : time.time()


    print('Rodando main')
    config = Config('data/configuration/', 'config')
    geral_config = config.get_configuration()
    print(geral_config)
    parser = Parser()
    model = Model(dict())
    print(f'Tempo de execução total: {elapsed_time(start)}')

if __name__ == '__main__':
    main()
