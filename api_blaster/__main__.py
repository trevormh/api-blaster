import configparser
import os

from api_blaster.app_configs import AppConfigs

ROOT_DIR = os.path.abspath(os.curdir)

# SETTINGS_DIR = f"{os.path.dirname(os.path.realpath(__file__))}/cli/commands/settings"
# REQUESTS_DIR = ''
# cfg_parser = configparser.ConfigParser()
#
#
# def get_requests_dir():
#     global REQUESTS_DIR
#     if not REQUESTS_DIR:
#         initialize_requests_dir()
#     return REQUESTS_DIR
#
#
# def initialize_requests_dir():
#     try:
#         cfg_parser.read(SETTINGS_DIR + '/requests_directory.ini')
#         requests_dir = cfg_parser['APP']['REQUESTS_DIRECTORY']
#         set_requests_dir(requests_dir)
#     except FileNotFoundError:
#         print('requests_directory.ini file not found, using default requests directory')
#         print(f'requests directory path: {REQUESTS_DIR}')
#     except Exception as exp:
#         print('Failed to initialize requests dir')


# def set_requests_dir(requests_dir: str) -> bool:
#     global REQUESTS_DIR
#     if os.path.isdir(requests_dir):
#         REQUESTS_DIR = requests_dir
#         return True
#     return False


def main():
    # initialize_requests_dir()  # make sure it updates each time its imported
    global ROOT_DIR
    cfg = AppConfigs(ROOT_DIR)
    from api_blaster.cli.cli import main
    main()


if __name__ == '__main__':  # pragma: nocover
    main()
