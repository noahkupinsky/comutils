import os
from comutils.config_file import ConfigFile
from comutils.pathy import DataManager
from comutils.cron_scheduler import CronScheduler, FunctionScheduler


CRON_SECTION = 'cron'


class CommandUser(DataManager):
    def __init__(self, name):
        super().__init__(name)
        self.config = ConfigFile(self.join('config.ini'))

    def configure(self, **settings):
        for key, value in settings.items():
            if value:
                self.config.set_config(key, value)


class CronUser(CommandUser, CronScheduler):
    def schedule_script(self, script_path, every_hours):
        script_interval_name = self._interval_name(script_path)
        if every_hours == self.config.get_config(script_interval_name):
            return
        super().schedule_script(script_path, every_hours)
        self.config.set_config(script_interval_name, every_hours, CRON_SECTION)

    def _interval_name(self, script_path):
        script_name_without_extension = os.path.splitext(os.path.basename(script_path))[0]
        script_interval_name = f'{script_name_without_extension}_interval'
        return script_interval_name
    
    
class FunctionSchedulerUser(CronUser, FunctionScheduler):
    pass
