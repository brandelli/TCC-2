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

def get_exact_precision(data):
    correct_relations = get_correct_relations(data)
    identified_relations = get_number_of_relations_predicted(data)
    return correct_relations/identified_relations

def get_exact_recall(data):
    correct_relations = get_correct_relations(data)
    total_relations = get_number_of_relations_in_dataset(data)
    return correct_relations/total_relations

def get_exact_f_measure(data):
    precision = get_exact_precision(data)
    recall = get_exact_recall(data)
    return (2*precision*recall)/(precision+recall)