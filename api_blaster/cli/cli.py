import cmd
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from api_blaster.settings.cfg import get_config
from api_blaster.cli.menu_builder import MenuBuilder
from api_blaster.cli.helpers import info, style_menu_items
from api_blaster.exit_codes import ExitCodes
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
        display_text = []
        for item in self.get_commands():
            commands.append(item)
            display_text.append(repr(item))
        return [commands, display_text]

    def print_menu(self, items):
        info(f"Directory: {self.menu.cur_directory_name()}")
        styled = style_menu_items(items)
        self.cmd.columnize(styled, displaywidth=80)

    def handle_hidden_cmd(self, cmd: str):
        if cmd == 'cd ..':
            if self.menu.get_dir() == get_config('SETTINGS_DIR'):
                # user was in settings menu and wants to exit, return to request directory
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
    menu = MenuBuilder(get_config('REQUESTS_DIR'))
    cli = CLI(menu)
    code = ExitCodes.SUCCESS.value
    while True:
        try:
            commands, display_text = cli.menu_items()
            cli.print_menu(commands)
            display_text.extend(cli.hidden_cmds)
            selection = prompt('> ', completer=WordCompleter(display_text))
            cli.handle_execute_command(selection)
        except (NameError, IOError) as err:
            from api_blaster.cli.helpers import critical
            critical(f"Failed to execute request.\n{err.args[0]}")
            code = ExitCodes.GENERAL_ERROR.value
            break
        except FileNotFoundError as err:
            from api_blaster.cli.helpers import critical
            print('file not found')  # TODO remove
            critical(err.args[0])
            code = ExitCodes.FILE_OR_DIR_NOT_FOUND.value
            break
        except (KeyboardInterrupt, EOFError):
            break  # Control-C or Control-D pressed
        except Exception as err:
            from api_blaster.cli.helpers import critical
            critical(f"Failed to execute request.\n{err.args[0]}")
            code = ExitCodes.GENERAL_ERROR.value
            break
    return code
