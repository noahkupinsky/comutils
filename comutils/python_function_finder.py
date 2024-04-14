import inspect
import os
import importlib.util
from comutils.pathy import EnsuredDirectory


class PythonFunctionFinder(EnsuredDirectory):
    def find_functions(self):
        return {
            name: function
            for module in self._find_modules()
            for name, function in inspect.getmembers(module, inspect.isfunction)
        }

    def _find_modules(self):
        return [
            self._get_module_from_file(file_name)
            for file_name in self._find_python_files()
        ]
    
    def _find_python_files(self):
        return [
            os.path.join(root, file_name)
            for root, _, files in os.walk(self.path)
            for file_name in files
            if file_name.endswith('.py')
        ]

    def _get_module_from_file(self, file_name):
        spec = self._get_module_spec_from_file(file_name)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    
    def _get_module_spec_from_file(self, file_name):
        module_name = file_name.replace('.py', '')
        file_path = os.path.join(self.path, file_name)
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        return spec