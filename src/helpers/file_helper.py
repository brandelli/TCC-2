import json
import csv
import xlrd

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


def convert_treino_propor_to_csv(original_file_path, new_file_path):
	fields = ['SENTENCE', 'POSITION_ARGUMENT_1', 'ARGUMENT_1', 'ARGUMENT_1_CATEGORY',
				'RELATION_POSITION', 'RELATION', 'POSITION_ARGUMENT_2', 'ARGUMENT_2', 'ARGUMENT_2_CATEGORY']

	with open(f'{original_file_path}') as fp:
		count_line = 2 # começa em 2 por causa do cabeçalho
		data_list = []
		for line in fp.readlines():
			local_dict = {}
			for index, column in enumerate(line.split('\t')):
				field = fields[index]
				if field == 'POSITION_ARGUMENT_1' or field == 'POSITION_ARGUMENT_2':
					if len(column.split(',')) > 1:			
						print(count_line)
				elif field == 'ARGUMENT_2_CATEGORY':
					column = column[:-1]
				elif field == 'RELATION':
					if len(column) == 0:
						column = 'None'

				local_dict[field] = column
			data_list.append(local_dict)
			count_line += 1

	with open(f'{new_file_path}', 'w') as fp:
		writer = csv.DictWriter(fp, fields, delimiter = '\t')
		writer.writeheader()
		writer.writerows(data_list)

	print(f'Finalizou conversão')


def convert_teste_propor_to_csv(original_file_path, new_file_path):
	wb = xlrd.open_workbook(original_file_path)
	sheet = wb.sheet_by_index(0)
	sheet.cell_value(0, 0)
	fields = [val for val in sheet.row_values(0)]
	print(fields)
	
	data_list = []
	for index in range(1, sheet.nrows):
		local_dict = {}
		for i, column in enumerate(sheet.row_values(index)):
			field = fields[i]
			if i < 2:
				column = int(column)	
			elif field == 'RELATION':
				if len(column) == 0:
					column = 'None'
			
			if field == 'SENTENCE':
				print(f'{column}')
			local_dict[field] = column
			
		data_list.append(local_dict)
	

	with open(f'{new_file_path}', 'w') as fp:
		writer = csv.DictWriter(fp, fields, delimiter = '\t')
		writer.writeheader()
		writer.writerows(data_list)

	print(f'Finalizou conversão')


def json_csv(path, file_name, new_file_name):
	fields = ['SENTENCE_ID', 'RELATION_ID', 'SENTENCE', 'ARGUMENT_1', 'ARGUMENT_1_CATEGORY', 'RELATION', 'PREDICTED_RELATION', 'ARGUMENT_2', 'ARGUMENT_2_CATEGORY']
	fields_dict = {
		'sentence_id' : 'SENTENCE_ID',
		'relation_id' : 'RELATION_ID',
		'predicted_relation' : 'PREDICTED_RELATION',
		'relation' : 'RELATION',
		'sentence' : 'SENTENCE'
	}
	dataset = get_json_file_data(path, file_name)
	data_list = []
	for data in dataset:
		local_dict = {}
		for key, value in data.items():
			if key != 'tail' and key != 'head':
				local_dict[fields_dict.get(key)] = value
			else:
				arg = 'ARGUMENT_1' if key == 'head' else 'ARGUMENT_2'
				cat = f'{arg}_CATEGORY'
				local_dict[arg] = value.get('word')
				local_dict[cat] = value.get('category')
		
		data_list.append(local_dict)
	
	with open(f'{path}{new_file_name}', 'w') as fp:
		writer = csv.DictWriter(fp, fields, delimiter = '\t')
		writer.writeheader()
		writer.writerows(data_list)

	print(f'Finalizou conversão')