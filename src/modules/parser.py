import csv
import json

def parse_iberlef_input(file_name):
    print(f"Rodando: {parse_iberlef_input.__name__}")
    input_dict = {}
    key_dict = {}
    with open(file_name) as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        keys = tsvreader.__next__()
        for index, key in enumerate(keys, start=0):
            input_dict[key] = []
            key_dict[index] = key

        for line in tsvreader:
            for index, word in enumerate(line, start=0):
                input_dict[key_dict[index]].append(word)

    return input_dict


def parse_dict_input_into_relation_id_mapping(input_dict):
    print(f"Rodando: {parse_dict_input_into_relation_id_mapping.__name__}")
    file_name = 'relation_id.json'
    count = 0
    relation_dict = {}
    relation_dict['NA'] = count
    count += 1
    relation_list = input_dict.get('RELATION')
    for value in relation_list:
        if relation_dict.get(value) is None:
            relation_dict[value] = count
            count += 1

    with open(file_name, 'w') as json_file:
        json.dump(relation_dict, json_file)


def parse_word_embeddings_input_to_json(file_name):
    word_list = []
    with open(file_name, 'r') as word_embeddings_file:
        lines, _ = word_embeddings_file.readline().strip().split(' ')
        print(lines)
        for x in range(0, int(lines)):
            print(x)
            word_dict = {}
            line = word_embeddings_file.readline().strip().split(' ')
            word_dict['word'] = line.pop(0)
            vector_list = []
            for val in line:
                vector_list.append(float(val))
            
            word_dict['vec'] = vector_list
            word_list.append(word_dict)

    with open('data/word_embeddings/word_embeddings.json', 'w') as json_file:
        json.dump(word_list, json_file, indent=0)
                 