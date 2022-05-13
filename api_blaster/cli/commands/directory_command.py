from api_blaster.cli.commands.command import Command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from api_blaster.cli.menu_builder import MenuBuilder


class DirectoryCommand(Command):

    def __init__(self, menu: 'MenuBuilder', dir_path):
        self.path = dir_path
        self.menu = menu

    def execute(self):
        # update the menu to use this directory's path
        self.menu.dir = self.path
        self.menu.update()

    def __repr__(self):
        return self.path.rpartition("/")[2]
