"""
Shifu client to call java module.
"""
from __future__ import print_function
from util.helper import Helper
from core.shell import Shell
from core.enums import CommandRunningStatus


class _Shifu(Shell):
    def __init__(self):
        super(_Shifu, self).__init__()

    def new(self, name, work_dir=None):
        self._init_working_directory(work_dir, name)
        command_list = ['sh', self._main_script, 'new', self._name]
        status, output = Helper.run_shell(command_list)
        if status is CommandRunningStatus.SUCCESS:
            self._change_to_model_dir()
            print("You can edit file:" + self._model_config_file)
            Helper.edit_file(self._os_platform, self._model_config_file)

    def __run_command(self, command):
        command_list = ['sh', self._main_script, command]
        Helper.run_shell(command_list)

    def init(self):
        self.__run_command("init")

    def stats(self):
        self.__run_command("stats")

    def norm(self):
        self.__run_command("norm")

    def varsel(self):
        self.__run_command("varsel")

    def train(self):
        self.__run_command("train")

    def eval(self):
        self.__run_command("eval")


shifu = _Shifu()


