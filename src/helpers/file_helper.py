import json
import csv

def dict_to_json(path, file_name, my_data, indent=0):
    '''
    Função para criar arquivo json com base em dados processados anteriormente
    '''
    with open(f'{path}{file_name}', 'w') as json_file:
        json.dump(my_data, json_file, indent=indent)


def get_json_file_data(path, file_name):
    '''
    Função para retornar um arquivo json em uma estrutura de dicionário
    '''
    json_data = {}    
    with open(f'{path}{file_name}') as json_file:
        json_data = json.load(json_file)
    
    return json_data


def save_txt_file(path, file_name, data):
    with open(f'{path}{file_name}', 'w') as txt_file:
        txt_file.write(data)


def convert_txt_to_csv(original_file_path, new_file_path):
	fields = ['SENTENCE', 'POSITION_ARGUMENT_1', 'ARGUMENT_1', 'ARGUMENT_1_CATEGORY',
				'RELATION_POSITION', 'RELATION', 'POSITION_ARGUMENT_2', 'ARGUMENT_2', 'ARGUMENT_2_CATEGORY']

	with open(f'{original_file_path}') as fp:
		count_line = 1
		data_list = []
		for line in fp.readlines():
			local_dict = {}
			for index, column in enumerate(line.split('\t')):
				field = fields[index]
				if field == 'POSITION_ARGUMENT_1' or field == 'POSITION_ARGUMENT_2':
					if len(column.split(',')) > 1:			
						print(count_line)
				if field == 'ARGUMENT_2_CATEGORY':
					column = column[:-1]
				local_dict[field] = column
			data_list.append(local_dict)
			count_line += 1

	with open(f'{new_file_path}', 'w') as fp:
		writer = csv.DictWriter(fp, fields, delimiter = '\t')
		writer.writeheader()
		writer.writerows(data_list)

	print(f'Finalizou conversão')