def get_correct_relations(data):
    count = 0
    for d in data:
        relation = d.get('relation').strip()
        predicted_relation = d.get('predicted_relation').strip()
        if relation == predicted_relation:
            count += 1

    return count

def get_number_of_relations_predicted(data):
    count = 0
    for d in data:
        if d.get('predicted_relation').strip() != '':
            count += 1

    return count

def get_number_of_relations_in_dataset(data):
    return len(data)