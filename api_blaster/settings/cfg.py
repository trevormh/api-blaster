import configparser, os

from api_blaster.settings.config_file_map import config_map

app_configs = {}


def initialize_configs(root_dir: str):
    app_configs['ROOT_DIR'] = root_dir
    app_configs['SETTINGS_DIRECTORY'] = os.path.join(root_dir, 'api_blaster', 'settings', 'configs')
    __load_config_files()


def __load_config_files():
    config = configparser.ConfigParser()
    for config_name, filename in config_map.items():
        __load_config(config, config_name, filename)


def __load_config(config_parser, config_name: str, config_filename: str):
    path = os.path.join(app_configs['SETTINGS_DIRECTORY'], config_filename)
    try:
        if not os.path.isfile(path):
            raise FileNotFoundError
        config_parser.read(path)
        requests_dir = config_parser['APP'][config_name]
        set_config(config_name, requests_dir)
    except FileNotFoundError:
        print(f'File not found: {path}')
    except Exception as exp:
        print(f'Failed to initialize {exp}')


def set_config(config_name: str, value: any):
    app_configs[config_name] = value
    return True


def get_config(config_name: str):
    return app_configs.get(config_name)
