from modules import parser
def main():
    print('Rodando main')
    input_dict = parser.parse_iberlef_input('data/treino/Corpus_RE_Treino.tsv')
    parser.parse_dict_input_into_relation_id_mapping(input_dict)
    parser.parse_word_embeddings_input_to_json('data/word_embeddings/glove_s50.txt')

if __name__ == '__main__':
    main()
