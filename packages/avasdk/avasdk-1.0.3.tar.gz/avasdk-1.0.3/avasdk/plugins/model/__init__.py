from ..log import Logger
from ..builders import build_request


class PythonModel(object):
    """
        Base Class of AVA python plugins
    """

    def __init__(self, name="AVA_Python_Plugin_Model"):
        super(PythonModel, self).__init__()
        PythonModel._commands = {
            "name": self.get_name,
            "list": self.list_commands,
            "commands": self.get_commands,
            "interaction": self.wait_for_user
        }
        PythonModel._name = name

    def set_commands_list(self, command_list):
        self._commands = command_list

    def get_name(self):
        return self._name

    def get_commands(self):
        return self._commands

    def list_commands(self):
        for c in self._commands:
            print(c)

    def wait_for_user(self, author, message=None, display=None):
        print(build_request(author, message, display))
        Logger.log_request()
        return input()
