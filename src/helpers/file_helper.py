from helpers import metrics_helper
import json
import csv
import xlrd
import xlsxwriter

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

def convert_avaliacao_propor_json(path, file_name, new_file_name, index_sheet=1):
	wb = xlrd.open_workbook(f'{path}{file_name}')
	sheet = wb.sheet_by_index(index_sheet)
	sheet.cell_value(0, 0)
	fields = [val for val in sheet.row_values(0)]

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
			
			local_dict[field] = column
			
		data_list.append(local_dict)
	

	dict_to_json(path, new_file_name, data_list)

	print(f'Finalizou conversão')
	

def get_metrics_propor(file_name='avaliacao.json', pair='Total'):
	file_data = get_json_file_data('data/propor/', file_name)
	total_relations = metrics_helper.get_total_relations_dataset(file_data)
	list_models = ['PREDICTED_RELATION REDES NEURAIS', 'PREDICTED_RELATION RelP modificada', 'PREDICTED_RELATION RelP e Redes Neurais Combinadas']
	print(f'---------------------{pair}-----------------------------')
	print(f'Total de relacionamentos no dataset: {total_relations}')

	for model in list_models:
		metrics_helper.print_all_metrics(metrics_helper.get_all_metrics(file_data, model), model)


def create_xlsx_from_json():
	data_file = get_json_file_data('data/output_files/', 'predicted_output_relp.json')
	workbook = xlsxwriter.Workbook('data/output_files/iberlef_output_relp.xlsx')
	worksheet = workbook.add_worksheet()
	row = 0
	col = 0
	header = ['sentence_id', 'sentence', 'argument_1', 'argument_1_category','relation', 'relation relp', 'argument_2', 'argument_2_category']
	for index, val in enumerate(header):
		worksheet.write(row, index, val)

	for data in data_file:
		print(data)

	workbook.close()


def create_xlsx_for_paper():
	wb = xlrd.open_workbook('data/propor/avaliacao.xlsx')
	sheet = wb.sheet_by_index(1)
	sheet.cell_value(0, 0)
	fields = [val for val in sheet.row_values(0)]
	fields_dict = {val:index for index, val in enumerate(sheet.row_values(0))}
	dict_tabs = {'original':[], 'org': [], 'plc': [], 'per':[]}

	for index in range(1, sheet.nrows):
		cur_row = sheet.row_values(index)
		dict_tabs.get('original').append(cur_row)
		arg_2_cat = cur_row[fields_dict.get('ARGUMENT_2_CATEGORY')]
		if arg_2_cat == 'ORG':
			dict_tabs.get('org').append(cur_row)
		elif arg_2_cat == 'PER':
			dict_tabs.get('per').append(cur_row)
		else:
			dict_tabs.get('plc').append(cur_row)
	
	workbook = xlsxwriter.Workbook('data/propor/avaliacao_lrec.xlsx')
	for key in dict_tabs:
		worksheet = workbook.add_worksheet(key)
		for index, field in enumerate(fields):
			worksheet.write(0, index, field)

		for index_row, row in enumerate(dict_tabs.get(key)):
			index_row += 1
			for index_col, col in enumerate(row):
				 worksheet.write(index_row, index_col, col)


	workbook.close()

	
def get_metrics_by_pair_lrec():
	tabs_list = ['Todas', 'ORG-ORG', 'ORG-PLC', 'ORG-PER']
	path = 'data/propor/'
	file_name = 'avaliacao_lrec.xlsx'
	for index, tab in enumerate(tabs_list):
		new_file_name = f'avaliacao_lrec_{tab}.json'
		convert_avaliacao_propor_json(path, file_name, new_file_name, index)
		get_metrics_propor(new_file_name, tab)
	
	