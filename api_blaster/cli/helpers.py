from enum import Enum, unique
from typing import List

from api_blaster.cli.commands.command import Command


#  https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
@unique
class CLI_COLORS(Enum):
    BLUE = '\33[34m'
    END = '\033[0m'
    GREEN = '\33[32m'
    RED = '\33[91m'
    YELLOW = '\33[33m'


def apply_info_style(message: str) -> str:
    return f"{CLI_COLORS['BLUE'].value}{message}{CLI_COLORS['END'].value}"


def info(message: str):
    print(apply_info_style(message), end="\n")


def apply_critical_style(message: str) -> str:
    return f"{CLI_COLORS['RED'].value}{message}{CLI_COLORS['END'].value}"


def critical(message: str):
    print(apply_critical_style(message), end="\n")


def apply_warn_style(message: str) -> str:
    return f"{CLI_COLORS['YELLOW'].value}{message}{CLI_COLORS['END'].value}"


def warn(message: str):
    message = f'YELLOW: {message}'
    print(f'{apply_warn_style(message)}', end="\n")


def alert(message: str):
    print(apply_warn_style(message), end="\n")


def apply_request_style(message: str) -> str:
    return f"{CLI_COLORS['GREEN'].value}{message}{CLI_COLORS['END'].value}"


def style_menu_items(items: List[Command]):
    styled = []
    for item in items:
        if type(item).__name__ == 'DirectoryCommand':
            styled.append(apply_info_style(repr(item)))
        elif type(item).__name__ == 'RequestCommand':
            styled.append(apply_request_style(repr(item)))
        else:
            styled.append(repr(item))
    return styled
