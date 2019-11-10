def get_correct_relations(data):
    count = 0
    for d in data:
        relation = d.get('relation').strip()
        predicted_relation = d.get('predicted_relation').strip()
        print(f'relation: {relation}')
        print(f'predicted_relation: {predicted_relation}')
        if relation == predicted_relation:
            count += 1

    return count

def get_partially_correct_relations(data):
    pcr_found = 0
    count = 0
    for d in data:
        relation = d.get('relation').strip()
        predicted_relation = d.get('predicted_relation').strip()
        if relation != predicted_relation and len(predicted_relation) > 0:
            pcr = calculate_partially_correct_relation(relation, predicted_relation)
            count += pcr
            if pcr > 0:
                pcr_found += 1

    print(f'Number of partially correct relations found: {pcr_found}')
    return count

def calculate_partially_correct_relation(relation, predicted_relation):
    split_relation = relation.split(' ')
    split_predict = predicted_relation.split(' ')
    count = 0
    max_len = max(len(split_relation), len(split_predict))
    for word in split_predict:
        if word in split_relation:
            count += 1

    return 0.5 * (count/max_len)


def get_number_of_relations_predicted(data):
    count = 0
    for d in data:
        if d.get('predicted_relation').strip() != '':
            count += 1

    return count

def get_number_of_relations_in_dataset(data):
    count = 0
    for d in data:
        relation = d.get('relation').strip()
        if relation != '' and relation != 'none':
            count += 1
    
    return count

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

def get_partial_precision(data):
    identified_relations = get_number_of_relations_predicted(data)
    correct_relations = get_correct_relations(data)
    partially_correct_relations = get_partially_correct_relations(data)
    return (correct_relations + partially_correct_relations) / identified_relations

def get_partial_recall(data):
    total_relations = get_number_of_relations_in_dataset(data)
    correct_relations = get_correct_relations(data)
    partially_correct_relations = get_partially_correct_relations(data)
    return (correct_relations + partially_correct_relations) / total_relations

def get_partial_f_measure(data):
    precision = get_partial_precision(data)
    recall = get_partial_recall(data)
    return (2*precision*recall)/(precision+recall)

def get_total_relations_dataset(data):
    count = 0
    for d in data:
        relation = d.get('RELATION MANUALLY')
        if relation != 'none':
            count += 1
    return count

def get_total_relations_by_approach(data, str_field):
    count = 0
    for d in data:
        relation = d.get(str_field)
        if relation != 'none' and len(relation) > 0:
            count += 1
    return count

def get_rcc(data, str_field):
    count = 0
    for d in data:
        relation = d.get('RELATION MANUALLY').strip()
        predicted_relation = d.get(str_field).strip()
        if relation == predicted_relation:
            count += 1

    return count

def get_rpc(data, str_field):
    rpc_found = 0
    count = 0
    for d in data:
        relation = d.get('RELATION MANUALLY').strip()
        predicted_relation = d.get(str_field).strip()
        if relation != predicted_relation and len(predicted_relation) > 0:
            rpc = calculate_partially_correct_relation(relation, predicted_relation)
            count += rpc
            if rpc > 0:
                rpc_found += 1

    return rpc_found, count

def get_exact_precision_propor(rcc, ri):
    return rcc/ri

def get_exact_recall_propor(rcc, rt):
    return rcc/rt

def get_exact_f_measure_propor(precisao, recall):
    return (2*precisao*recall)/(precisao+recall)

def get_partial_precision_propor(rcc, rpc, ri):
    return (rcc + rpc) / ri

def get_partial_recall_propor(rcc, rpc, rt):
    return (rcc + rpc) / rt

def get_partial_f_measure_propor(precisao, recall):
    return (2*precisao*recall)/(precisao+recall)