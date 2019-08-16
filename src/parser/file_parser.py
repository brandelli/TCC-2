import csv

def parse_iberlef_input(file_name):
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

