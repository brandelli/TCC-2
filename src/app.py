from parser import file_parser
def main():
    """
    Módulo main
    """
    print('teste')
    print(file_parser.parse_iberlef_input('data/dataset/Task2-Corpus-Test1.tsv'))

if __name__ == '__main__':
    main()
