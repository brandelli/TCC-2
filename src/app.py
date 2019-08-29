import time
from helpers import file_helper, time_helper
from modules.parser import Parser
def main():
    start = time.time()
    print('Rodando main')
    # treino, teste_1, teste_2
    dataset_path = 'data/dataset/'
    parser = Parser()
    start_process = time.time()
    parser.dataset_to_json(dataset_path,'treino')
    print(f'Finalizou dataset_treino: {time_helper.get_elapsed_time(start_process)}')
    start_process = time.time()
    parser.dataset_to_json(dataset_path, 'teste_1')
    print(f'Finalizou dataset_teste: {time_helper.get_elapsed_time(start_process)}')
    start_process = time.time()
    parser.word_embeddings_to_json('data/word_embeddings/exemplo/', 'word_embeddings')
    print(f'Finalizou word_embeddings_to_json: {time_helper.get_elapsed_time(start_process)}')
    start_process = time.time()
    parser.relation_to_id('data/dataset/', 'treino')
    print(f'Finalizou relation_to_id: {time_helper.get_elapsed_time(start_process)}')
    start_process = time.time()
    parser.create_word_to_id()
    print(f'Finalizou word_to_id: {time_helper.get_elapsed_time(start_process)}')
    start_process = time.time()
    print(f'Tempo de execução total: {time_helper.get_elapsed_time(start)}')

if __name__ == '__main__':
    main()
