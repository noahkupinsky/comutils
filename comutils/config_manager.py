import configparser
import json
import os

class ConfigManager:
    DEFAULT_SECTION = 'config'

    def __init__(self, path):
        self.path = path
        self.config = configparser.ConfigParser()
        self._setup()
        
    
    def _setup(self):
        if not os.path.exists(self.path):
            self._write()
        else:
            self.config.read(self.path)

    def _ensure_section_exists(self, section):
        if not self.config.has_section(section):
            self.config.add_section(section)

    def _write(self):
        with open(self.path, 'w') as config_file:
            self.config.write(config_file)

    def get_value(self, key, section=DEFAULT_SECTION, parse_json=False):
        self._ensure_section_exists(section)
        value = self.config.get(section, key)
        if parse_json and self._is_json_string(value):
            value = json.loads(value)
        return value
    
    def get_or_set_default(self, key, default_value, section=DEFAULT_SECTION, parse_json=False):
        if self.config.has_option(section, key):
            return self.get_value(key, section, parse_json)
        else:
            self.set_value(key, default_value, section)
            return default_value

    def set_value(self, key, value, section=DEFAULT_SECTION):
        if not isinstance(value, str):
            value = json.dumps(value)
        self._ensure_section_exists(section)
        self.config.set(section, key, value)
        self._write()

    def _is_json_string(self, value):
        return value.startswith("{") and value.endswith("}")