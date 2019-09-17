import time
from helpers import file_helper, time_helper
from modules.parser import Parser
from modules.model import Model
def main():
    model = Model(dict())
    start = time.time()
    elapsed_time = lambda start_time: time_helper.get_elapsed_time(start_time)
    print_elapsed_time = lambda process, start_time: print(f'Finalizou {process} {elapsed_time(start_time)}')
    get_time = lambda : time.time()
    print('Rodando main')
    # treino, teste_1, teste_2
    dataset_path = 'data/dataset/'
    parser = Parser()
    configs = parser.get_configs('data/configuration/', 'config')
    print(configs)
    start_process = get_time()
    parser.dataset_to_json(dataset_path,'treino')
    print_elapsed_time('dataset_treino', start_process)
    start_process = get_time()
    parser.dataset_to_json(dataset_path, 'teste_1')
    print_elapsed_time('dataset_teste', start_process)
    start_process = get_time()
    parser.word_embeddings_to_json('data/word_embeddings/exemplo/', 'word_embeddings')
    print_elapsed_time('word_embeddings_to_json', start_process)
    start_process = get_time()
    parser.relation_to_id('data/dataset/', 'treino')
    print_elapsed_time('relation_to_id', start_process)
    start_process = get_time()
    parser.create_word_to_id()
    print_elapsed_time('word_to_id', start_process)
    start_process = get_time()
    print(f'Tempo de execução total: {elapsed_time(start)}')

if __name__ == '__main__':
    main()
