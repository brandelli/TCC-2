def create_dataset_dict():
    return {
        'sentence_id': None,
        'sentence': None,
        'head': {
            'word': None,
            'id': None,
            'category': None
        },
        'tail': {
            'word': None,
            'id': None,
            'category': None
        },
        'relation': None,
        'relation_id': None
    }