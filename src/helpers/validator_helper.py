def is_entity(key):
    return key == 'argument_1' or key == 'argument_2'

def is_category(key):
    return key == 'argument_1_category' or key == 'argument_2_category'

def is_sentence(key):
    return key == 'sentence'

def is_relation(key):
    return key == 'relation'

def is_id_data(key):
    return key == 'sentence_id' or key == 'relation_id'