from appdirs import user_data_dir
import os


class DataManager:
    def __init__(self, name):
        self.name = name
        self.dir = user_data_dir(name)
        os.makedirs(self.dir, exist_ok=True)
    
    def get_path(self, file_name):
        return os.path.join(self.dir, file_name)