from helpers import file_helper
class Parser:

    relation_id = 0
    word_id = 1

    def increment_relation_id(self, inc=1):
        self.relation_id += inc


    def increment_word_id(self, inc=1):
        self.word_id += inc

    def relation_to_id(self, path, file_name):
        treino_json = file_helper.get_json_file_data(path, file_name)
        relation_list = treino_json.get('relation')
        relation_dict = {}
        relation_dict['NA'] = self.relation_id
        for relation in relation_list:
            if relation_dict.get(relation) is None:
                self.increment_relation_id()
                relation_dict[relation] = self.relation_id
        
        file_helper.dict_to_json('data/relation/', 'relation_2_id', relation_dict, 4)
        
        
