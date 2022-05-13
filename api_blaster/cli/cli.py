import cmd
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from api_blaster.__main__ import ROOT_DIR
from api_blaster.cli.menu_builder import MenuBuilder

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from api_blaster.cli.commands.command import Command


class CLI:

    nav_cmds = ['cd ..', 'exit']

    def __init__(self, menu: MenuBuilder):
        self.commands: list['Command'] = []
        self.menu = menu
        self.items = []
        self.cmd = cmd.Cmd()

    def get_commands(self) -> List['Command']:
        return self.menu.get_items()

    def menu_items(self) -> List[str]:
        menu_items = []
        for item in self.get_commands():
            menu_items.append(repr(item))
        return menu_items

    def print_menu(self, items):
        print(f"Directory: {self.menu.cur_directory()}")
        self.cmd.columnize(items, displaywidth=50)

    def handle_nav(self, cmd: str):
        if cmd == 'cd ..':
            self.menu.nav_up()
        if cmd == 'exit':
            raise KeyboardInterrupt

    def execute(self, cmd: str):
        if not cmd:
            return
        elif cmd in self.nav_cmds:
            return self.handle_nav(cmd)
        try:
            idx = self.menu_items().index(cmd)
            self.get_commands()[idx].execute()
        except ValueError:
            print(f"Item '{cmd}' not found", end="\n\n")


def main():
    collections_dir = f"{ROOT_DIR}/request_collections"
    menu = MenuBuilder(collections_dir)
    cli = CLI(menu)
    while True:
        try:
            items = cli.menu_items()
            cli.print_menu(items)
            items.extend(cli.nav_cmds)
            selection = prompt('%s> ', completer=WordCompleter(items))
            cli.execute(selection)
        except KeyboardInterrupt:
            break  # Control-C pressed
        except EOFError:
            break  # Control-D pressed
