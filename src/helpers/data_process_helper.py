def process_entity_data(cur_dict, key, value):
    entity = cur_dict.get('head') if key == 'argument_1' else cur_dict.get('tail')
    entity['word'] = value.lower()

def process_category_data(cur_dict, key, value):
    entity = cur_dict.get('head') if key == 'argument_1_category' else cur_dict.get('tail')
    entity['category'] = value

def process_sentence_data(cur_dict, key, value):
    cur_dict[key] = value.lower()

def process_relation_data(cur_dict, key, value):
    cur_dict[key] = value.lower()

def process_id_data(cur_dict, key, value):
    cur_dict[key] = int(value)