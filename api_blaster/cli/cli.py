import cmd
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from api_blaster.__main__ import ROOT_DIR
from api_blaster.cli.menu_builder import MenuBuilder
from api_blaster.cli.helpers import info, style_menu_items
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

    def get_commands(self):
        return self.menu.get_items()

    def menu_items(self):
        menu_items = []
        commands = []
        for item in self.get_commands():
            menu_items.append(repr(item))
            commands.append(item)
        return [commands, menu_items]

    def print_menu(self, items):
        info(f"Directory: {self.menu.cur_directory()}")
        styled = style_menu_items(items)
        # breakpoint()
        self.cmd.columnize(styled, displaywidth=80)

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
            _, commands = self.menu_items()
            idx = commands.index(cmd)
            self.get_commands()[idx].execute()
        except ValueError:
            print(f"Item '{cmd}' not found", end="\n\n")


def main():
    collections_dir = f"{ROOT_DIR}/request_collections"
    menu = MenuBuilder(collections_dir)
    cli = CLI(menu)
    while True:
        try:
            commands, items = cli.menu_items()
            cli.print_menu(commands)
            items.extend(cli.nav_cmds)
            selection = prompt('> ', completer=WordCompleter(items))
            cli.execute(selection)
        except (FileNotFoundError, NameError, IOError) as err:
            from api_blaster.cli.helpers import critical
            critical(f"Failed to execute request.\n{err.args[0]}")
            break
        except (KeyboardInterrupt, EOFError):
            break  # Control-C or Control-D pressed
        except Exception as err:
            from api_blaster.cli.helpers import critical
            critical(f"Failed to execute request.\n{err.args[0]}")
            break
