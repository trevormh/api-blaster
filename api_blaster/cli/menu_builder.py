from api_blaster.settings.cfg import get_config
import os
from typing import List, TYPE_CHECKING, Union

from api_blaster.cli.commands.settings_command import SettingsCommand
from api_blaster.cli.helpers import critical
# from api_blaster.settings.config_file_map import config_file_map

if TYPE_CHECKING:
    from api_blaster.cli.commands.command import Command

from api_blaster.cli.commands.directory_command import DirectoryCommand
from api_blaster.cli.commands.request_command import RequestCommand


class MenuBuilder:
    exclude = ['.env', '.DS_Store', '__init__.py', '__pycache__']

    def __init__(self, collections_dir):
        self.dir = collections_dir
        self.commands = []
        self.dot_env_path = None
        self._set_dot_env_path()
        self._set_commands()
        self.requests_dir = get_config('REQUESTS_DIR')

    def set_dir(self, new_dir: str):
        self.dir = new_dir
        self._set_commands()

    def get_dir(self):
        return self.dir

    def _set_commands(self):
        commands = self._read_contents()
        self._set_dot_env_path()
        self.commands = self.__create_menu_commands(commands)

    def get_items(self):
        return self.commands

    def nav_up(self):
        # don't allow backing out beyond the requests directory!
        requests_dir = self.requests_dir
        if self.dir != requests_dir:
            self.set_dir(self.dir.rpartition("/")[0])
            # self._set_commands()

    def cur_directory_name(self):
        return self.dir.rpartition("/")[2]

    def _set_dot_env_path(self):
        if os.path.isfile(f"{self.dir}/.env"):
            self.dot_env_path = f"{self.dir}/.env"

    def _read_contents(self) -> Union[List[str], None]:
        try:
            return os.listdir(self.dir)
        except FileNotFoundError as e:
            critical(e.args[1])
            return None

    def __create_menu_commands(self, items):
        commands: List['Command'] = []
        for item in items:
            item_path = f"{self.dir}/{item}"
            if item in self.exclude:
                continue
            elif self.dir == get_config('SETTINGS_DIR'):
                commands.append(SettingsCommand(filename=item))
            elif os.path.isdir(item_path):
                commands.append(DirectoryCommand(self, item_path))
            elif os.path.isfile(item_path):
                commands.append(RequestCommand(self, self.dir, item))
        return commands

    def update(self):
        self._set_commands()
