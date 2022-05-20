from api_blaster.__main__ import ROOT_DIR
import os
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from api_blaster.cli.commands.command import Command

from api_blaster.cli.commands.directory_command import DirectoryCommand
from api_blaster.cli.commands.request_command import RequestCommand


class MenuBuilder:
    reserved_names = ['environment.json']

    def __init__(self, current_dir):
        self.dir = current_dir
        self.items = []
        self.environment_path = None
        self._set_environment_path()

        self._set_items()

    def _set_items(self):
        items = self._read_contents()
        self._set_environment_path()
        self.items = self._create_menu_commands(items)

    def get_items(self):
        return self.items

    def nav_up(self):
        if self.dir != ROOT_DIR:
            self.dir = self.dir.rpartition("/")[0]
            self._set_items()

    def cur_directory(self):
        return self.dir.rpartition("/")[2]

    def _set_environment_path(self):
        if os.path.isfile(f"{self.dir}/environment.json"):
            self.environment_path = f"{self.dir}/environment.json"

    def _read_contents(self) -> List[str]:
        return os.listdir(self.dir)

    def _create_menu_commands(self, items):
        menu_items: List['Command'] = []
        for item in items:
            item_path = f"{self.dir}/{item}"
            if os.path.isdir(item_path):
                menu_items.append(DirectoryCommand(self, item_path))
            elif os.path.isfile(item_path):
                if item not in self.reserved_names:
                    menu_items.append(RequestCommand(self, item_path))
        return menu_items

    def update(self):
        self._set_items()