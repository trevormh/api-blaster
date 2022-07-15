import configparser
import os

from api_blaster.cli.helpers import warn

ROOT_DIR = os.path.abspath(os.curdir)

SETTINGS_DIR = f"{os.path.dirname(os.path.realpath(__file__))}/cli/commands/settings"
REQUESTS_DIR = f'{ROOT_DIR}/config.ini'
config = configparser.ConfigParser()


def get_requests_dir():
    global REQUESTS_DIR
    return REQUESTS_DIR


def initialize_requests_dir():
    try:
        config.read(SETTINGS_DIR + '/update_requests_directory.ini')
        requests_dir = config['APP']['REQUESTS_DIRECTORY']
        set_requests_dir(requests_dir)
    except FileNotFoundError:
        print('update_requests_directory.ini file not found, using default requests directory')
        print(f'requests directory path: {REQUESTS_DIR}')
    except Exception as exp:
        print('Failed to initialize requests dir')


def set_requests_dir(requests_dir: str) -> bool:
    global REQUESTS_DIR
    if os.path.isdir(requests_dir):
        REQUESTS_DIR = requests_dir
        return True
    return False


def main():
    initialize_requests_dir()  # make sure it updates each time its imported
    from api_blaster.cli.cli import main
    main()


if __name__ == '__main__':  # pragma: nocover
    main()
