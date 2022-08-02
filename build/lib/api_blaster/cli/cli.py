import cmd
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from api_blaster.settings.cfg import get_config
from api_blaster.cli.menu_builder import MenuBuilder
from api_blaster.cli.helpers import info, style_menu_items
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from api_blaster.cli.commands.command import Command


class CLI:

    hidden_cmds = ['cd ..', 'exit', 'settings']

    def __init__(self, menu: MenuBuilder):
        self.commands: list['Command'] = []
        self.menu = menu
        self.items = []
        self.cmd = cmd.Cmd()

    def get_commands(self):
        return self.menu.get_items()

    def menu_items(self):
        commands = []
        menu_items = []
        for item in self.get_commands():
            commands.append(item)
            menu_items.append(repr(item))
        return [commands, menu_items]

    def print_menu(self, items):
        info(f"Directory: {self.menu.cur_directory()}")
        styled = style_menu_items(items)
        self.cmd.columnize(styled, displaywidth=80)

    def handle_hidden_cmd(self, cmd: str):
        if cmd == 'cd ..':
            if self.menu.cur_directory() == "settings":
                # user exited settings, return to request directory
                request_dir = get_config('REQUESTS_DIR')
                self.menu.set_dir(request_dir)
            else:
                self.menu.nav_up()
        elif cmd == 'exit':
            raise KeyboardInterrupt
        elif cmd == "settings":
            settings_dir = get_config('SETTINGS_DIR')
            self.menu.set_dir(settings_dir)

    def handle_execute_command(self, cmd: str):
        if not cmd:
            return
        elif cmd in self.hidden_cmds:
            return self.handle_hidden_cmd(cmd)
        else:
            try:
                _, commands = self.menu_items()
                idx = commands.index(cmd)
                self.get_commands()[idx].execute()
            except ValueError:
                from api_blaster.cli.helpers import warn
                warn(f"Item '{cmd}' not found")


def main():
    print('in main')
    print(get_requests_dir())
    menu = MenuBuilder(get_requests_dir())
    cli = CLI(menu)
    while True:
        try:
            commands, items = cli.menu_items()
            cli.print_menu(commands)
            items.extend(cli.hidden_cmds)
            selection = prompt('> ', completer=WordCompleter(items))
            cli.handle_execute_command(selection)
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
