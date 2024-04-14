import configparser
import json
from comutils.pathy import EnsuredFile


DEFAULT_SECTION = 'config'


class ConfigFile(EnsuredFile):
    def __init__(self, config_file_path):
        super().__init__(config_file_path)
        self.config = configparser.ConfigParser()
        self.config.read(config_file_path)

    def _ensure_section_exists(self, section):
        if not self.config.has_section(section):
            self.config.add_section(section)

    def _write(self):
        with open(self.path, 'w') as config_file:
            self.config.write(config_file)

    def _get_value(self, section, key):
        self._ensure_section_exists(section)
        value = self.config.get(section, key)
        return value
    
    def has_config(self, key, section=DEFAULT_SECTION):
        return self.config.has_option(section, key)
    
    def get_config(self, key, fallback=None, section=DEFAULT_SECTION):
        if self.config.has_option(section, key):
            return self._get_value(section, key)
        elif fallback is not None:
            self.set_config(key, fallback, section)
        return fallback

    def set_config(self, key, value, section=DEFAULT_SECTION):
        self._ensure_section_exists(section)
        self.config.set(section, key, value)
        self._write()
        