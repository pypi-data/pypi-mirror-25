import unittest
import os
from shifu.util.helper import Helper


class TestHelper(unittest.TestCase):
    def setUp(self):
        self._current_script_path = os.path.dirname(os.path.abspath(__file__))

    def test_get_current_path(self):
        status, result = Helper.run_shell(['pwd', ])
        self.assertEqual(Helper.get_current_path(), result.strip())

    def test_run_shell(self):
        status, result = Helper.run_shell(['pwd', ])
        self.assertEqual(result.strip(), Helper.get_environment_variable("PWD"))

    def test_get_environment_variable(self):
        self.assertEqual(Helper.get_environment_variable("PWD"), Helper.get_current_path())

    def test_exist_file_in_current_path(self):
        self.assertTrue(Helper.exist_file_in_current_path("__init__.py"))

    def test_get_shifu_home(self):
        self.assertEqual(Helper.get_shifu_home().split('/')[-1], "shifu")

    def test_set_os_environment(self):
        Helper.set_os_environment("SHIFU_HOME", "wu")
        self.assertEqual(Helper.get_environment_variable("SHIFU_HOME"), "wu")

    def test_list_files_in_directory(self):
        self.assertEqual(len(Helper.list_files_in_directory(Helper.get_shifu_home(), True, "py")), 2)


if __name__ == '__main__':
    unittest.main()
