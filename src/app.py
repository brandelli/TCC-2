from helpers import file_helper
def main():
    print('Rodando main')
    # treino, teste_1, teste_2
    input_dict = file_helper.tsv_to_json('data/dataset/','treino')

if __name__ == '__main__':
    main()
