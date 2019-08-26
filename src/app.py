from helpers import file_helper
from modules.parser import Parser
def main():
    print('Rodando main')
    # treino, teste_1, teste_2
    dataset_path = 'data/dataset/'
    parser = Parser()
    parser.tsv_to_json(dataset_path,'treino')
    parser.tsv_to_json(dataset_path, 'teste_1')
    parser.word_embeddings_to_json('data/word_embeddings/exemplo/', 'word_embeddings')
    parser.relation_to_id('data/dataset/', 'treino')

if __name__ == '__main__':
    main()
