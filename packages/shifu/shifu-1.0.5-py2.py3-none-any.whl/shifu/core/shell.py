from shifu.util.helper import Helper
from os import path, getcwd, chdir


class Shell(object):
    def __init__(self):
        self._name = None  # set value when start run command new
        self._work_dir = None  # set value when finish run command new
        self._model_dir = None
        self._model_config_file = None  # set value when work dir ready
        self._model_config_file_name = "ModelConfig.json"
        self._os_platform = Helper.get_os_platform()
        self._shifu_home = Helper.get_shifu_home()
        self._main_script = path.join(self._shifu_home, "java", "bin", "shifu")

    def _sanity_check(self):
        if self._model_config_file is None or not path.exists(self._model_config_file):
            print('[Error] This is not a model set folder because no ModelConfig.json found in working dir: %s, '
                  'please change folder to your model set folder.' % self._work_dir)
            return False
        return True

    def _change_to_model_dir(self):
        if self._model_dir is None:
            raise ValueError("Model dir is not set!")
        chdir(self._model_dir)
        print("Directory changed to " + getcwd())

    def __set_work_dir(self, work_dir):
        if work_dir is None:
            work_dir = getcwd()
        self._work_dir = work_dir

    def __set_model_name(self, model_name):
        if model_name is None:
            raise ValueError("Model name can not be None!")
        if self._work_dir is None:
            raise ValueError("Setting model name while working dir is None!")
        self._name = model_name
        self._model_dir = path.join(self._work_dir, self._name)
        self._model_config_file = path.join(self._model_dir, self._model_config_file_name)

    def _init_working_directory(self, work_directory, model_name):
        self.__set_work_dir(work_directory)
        self.__set_model_name(model_name)





