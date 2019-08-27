def process_entity_data(cur_dict, key, value):
    print(f'{process_entity_data.__name__}')
    entity = cur_dict.get('head') if key == 'argument_1' else cur_dict.get('tail')
    entity['word'] = value.lower()

def process_category_data(cur_dict, key, value):
    print(f'{process_category_data.__name__}')
    entity = cur_dict.get('head') if key == 'argument_1_category' else cur_dict.get('tail')
    entity['category'] = value

def process_sentence_data(cur_dict, key, value):
    print(f'{process_sentence_data.__name__}')
    cur_dict['sentence'] = value.lower()

def process_relation_data(cur_dict, key, value):
    print(f'{process_relation_data.__name__}')
    cur_dict['relation'] = value.lower()