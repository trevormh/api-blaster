import configparser
import os

ROOT_DIR = os.path.abspath(os.curdir)

SETTINGS_DIR = f"{os.path.dirname(os.path.realpath(__file__))}/cli/commands/settings"

COLLECTIONS_DIR = ''
config = configparser.ConfigParser()
try:
    config.read(ROOT_DIR + '/config.ini')

    # config['APP']['REQUESTS_DIRECTORY'] = '/Users/trevorholloway/software_dev/api_blaster_requests'
    # with open(ROOT_DIR + '/config.ini', 'w') as configfile:
    #     config.write(configfile)

    REQUESTS_DIR = config['APP']['REQUESTS_DIRECTORY']
except FileNotFoundError:
    print('config.ini file not found.')
except Exception as exp:
    print('here')



def main():
    from api_blaster.cli.cli import main
    main()


if __name__ == '__main__':  # pragma: nocover
    main()
