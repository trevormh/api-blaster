from typing import List

from api_blaster.cli.commands.command import Command


#  https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
class CLI_COLORS:
    CRITICAL = '\33[91m'  # red
    END = '\033[0m'
    REQUEST = '\33[32m' # Green
    INFO = '\33[34m'  # Blue
    WARNING = '\33[33m'  # yellow


def apply_info_style(message: str) -> str:
    return f"{CLI_COLORS.INFO}{message}{CLI_COLORS.END}"


def info(message: str):
    print(apply_info_style(message), end="\n")


def apply_critical_style(message: str) -> str:
    return f"{CLI_COLORS.CRITICAL}{message}{CLI_COLORS.END}"


def critical(message: str):
    print(apply_critical_style(message), end="\n")


def apply_warn_style(message: str) -> str:
    return f"{CLI_COLORS.WARNING}{message}{CLI_COLORS.END}"


def warn(message: str):
    message = f'WARNING: {message}'
    print(f'{apply_warn_style(message)}', end="\n")


def alert(message: str):
    print(apply_warn_style(message), end="\n")


def apply_request_style(message: str) -> str:
    return f"{CLI_COLORS.REQUEST}{message}{CLI_COLORS.END}"


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
