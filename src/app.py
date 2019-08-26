from helpers import file_helper
from modules.parser import Parser
def main():
    print('Rodando main')
    # treino, teste_1, teste_2
    dataset_path = 'data/dataset/'
    file_helper.tsv_to_json(dataset_path,'treino')
    file_helper.tsv_to_json(dataset_path, 'teste_1')
    file_helper.word_embeddings_to_json('data/word_embeddings/exemplo/', 'word_embeddings')
    parser = Parser()
    parser.relation_to_id('data/dataset/', 'treino')

if __name__ == '__main__':
    main()
