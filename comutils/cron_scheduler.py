from comutils.pathy import EnsuredDirectory, EnsuredFile
import os
import shlex


DEFAULT_EVERY_HOURS = 8


class PythonExecutor(EnsuredFile):
    def __init__(self, path, python_path):
        super().__init__(path)
        self.write(f'#!/bin/bash\npython3 "{python_path}"\n')
        os.chmod(self.path, 0o755)


class CronScheduler(EnsuredDirectory):
    def schedule_script(self, script_path, every_hours):
        if int(every_hours) <= 0:
            raise ValueError(f"{every_hours} <= 0")
        self._remove_existing_schedulings(script_path)
        cron_command = f'0 */{every_hours.strip()} * * * {shlex.quote(script_path)}'
        os.system(f'echo "{cron_command}" | crontab -')

    def _remove_existing_schedulings(self, script_path):
        os.system(f'crontab -l | grep -v "{script_path}" | crontab -')
    

class FunctionScheduler(CronScheduler):
    def __init__(self, path):
        super().__init__(path)

    def schedule_function(self, package, function, every_hours):
        python_path = self._create_python_file(package, function)
        executor_path = PythonExecutor(self.join(f'{package}_{function}_executor.sh'), python_path).path
        self.schedule_script(executor_path, every_hours)

    def _create_python_file(self, package, function):
        content = f'import {package}\n{package}.{function}()\n'
        python_path = self.join(f'{package}_{function}.py')
        EnsuredFile(python_path).write(content)
        return python_path

