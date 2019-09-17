from helpers import file_helper

class Config:

    def __init__(self, path, file_name):
        self.config = file_helper.get_json_file_data(path, file_name)

    def get_configuration(self):
        return self.config
