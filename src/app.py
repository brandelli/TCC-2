from parser import file_parser
def main():
    print('Rodando main')
    input_dict = file_parser.parse_iberlef_input('data/treino/Corpus_RE_Treino.tsv')
    file_parser.parse_dict_input_into_relation_id_mapping(input_dict)

if __name__ == '__main__':
    main()
