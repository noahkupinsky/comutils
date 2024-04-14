import os
import shutil
from appdirs import user_data_dir


class Pathy:
    def __init__(self, path):
        self.path = path

    def join(self, *args):
        return os.path.join(self.path, *args)


class EnsuredDirectory(Pathy):
    def __init__(self, path):
        super().__init__(path)
        os.makedirs(path, exist_ok=True)


class EnsuredFile(Pathy):
    def __init__(self, path):
        super().__init__(path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'a').close()

    def write(self, content):
        with open(self.path, 'w') as f:
            f.write(content)


class CopyDirectory(Pathy):
    def copy_file(self, file_path, relative_folder_dest):
        file_name = os.path.basename(file_path)
        dest_path = self.join(relative_folder_dest, file_name)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copy(file_path, dest_path)


class DataManager(EnsuredDirectory):
    def __init__(self, name):
        super().__init__(user_data_dir(name))
        self.name = name