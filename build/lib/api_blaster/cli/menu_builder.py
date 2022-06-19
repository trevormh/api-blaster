from api_blaster.__main__ import ROOT_DIR, SETTINGS_DIR
import os
from typing import List, TYPE_CHECKING

from api_blaster.cli.commands.settings_command import SettingsCommand
# from api_blaster.cli.commands.settings_menu_command import SettingsMenuCommand

if TYPE_CHECKING:
    from api_blaster.cli.commands.command import Command

from api_blaster.cli.commands.directory_command import DirectoryCommand
from api_blaster.cli.commands.request_command import RequestCommand


class MenuBuilder:
    exclude = ['.env', '.DS_Store', '__init__.py']

    def __init__(self, collections_dir):
        self.dir = collections_dir
        self.commands = []
        self.dot_env_path = None
        self._set_dot_env_path()
        self._set_commands()

    def set_dir(self, new_dir: str):
        self.dir = new_dir
        self._set_commands()

    def _set_commands(self):
        commands = self._read_contents()
        self._set_dot_env_path()
        self.commands = self._create_menu_commands(commands)

    def get_items(self):
        return self.commands

    def nav_up(self):
        if self.dir != ROOT_DIR:
            self.set_dir(self.dir.rpartition("/")[0])
            # self._set_commands()

    def cur_directory(self):
        return self.dir.rpartition("/")[2]

    def _set_dot_env_path(self):
        if os.path.isfile(f"{self.dir}/.env"):
            self.dot_env_path = f"{self.dir}/.env"

    def _read_contents(self) -> List[str]:
        return os.listdir(self.dir)

    def _create_menu_commands(self, items):
        commands: List['Command'] = []
        for item in items:
            item_path = f"{self.dir}/{item}"
            if item in self.exclude:
                continue
            elif self.dir == SETTINGS_DIR:
                commands.append(SettingsCommand(item))
            elif os.path.isdir(item_path):
                commands.append(DirectoryCommand(self, item_path))
            elif os.path.isfile(item_path) and item not in self.exclude:
                commands.append(RequestCommand(self, self.dir, item))
        return commands

    def update(self):
        self._set_commands()
