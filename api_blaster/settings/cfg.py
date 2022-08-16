import configparser, os
from distutils.util import strtobool

from api_blaster.settings.config_file_map import ConfigFileName

# global dict for configs/settings in the form of SETTING_NAME:VALUE
app_configs = {}
# global dict to provide info about settings in the form of SETTING_NAME:INFO
app_configs_info = {}


def initialize_configs(root_dir: str):
    app_configs['ROOT_DIR'] = root_dir
    app_configs['SETTINGS_DIR'] = os.path.join(root_dir, 'api_blaster', 'settings', 'configs')
    __load_config_files()


def __load_config_files():
    config = configparser.ConfigParser()
    for cfg in ConfigFileName:
        __load_config(config, cfg.name, cfg.value)


def __load_config(config_parser, config_name: str, config_filename: str):
    path = os.path.join(app_configs['SETTINGS_DIR'], config_filename)
    try:
        if not os.path.isfile(path):
            raise FileNotFoundError
        config_parser.read(path)
        requests_dir = config_parser['APP'][config_name]
        if 'INFO' in config_parser['APP']:
            app_configs_info[config_name] = config_parser['APP']['INFO']
        set_app_config(config_name, requests_dir)
    except FileNotFoundError:
        print(f'File not found: {path}')
    except Exception as exp:
        print(f'Failed to initialize {exp}')


# sets config name and config value in the global app_configs dictionary
def set_app_config(config_name: str, value: any):
    try:
        # print(config_name, value)
        # config values are strings, "cast" to bool when encountered
        if value in ['True', 'False']:
            value = strtobool(value)
        app_configs[config_name] = value
        return True
    except Exception as e:
        print(f'Failed to set app config for {config_name}')


def get_config(config_name: str):
    return app_configs.get(config_name)


def get_config_info(config_name: str):
    return app_configs_info.get(config_name)


# updates both the config file and global config dict
def update_config(file: str, config_name: str, value: str):
    if __update_config_file(file, config_name, value):
        if set_app_config(config_name, value):
            return True


def __update_config_file(path: str, name: str, value: str) -> bool:
    config = configparser.ConfigParser()
    config.read(path)
    try:
        with open(path, 'w') as configfile:
            config['APP'][name] = value
            config.write(configfile)
            return True
    except FileNotFoundError as e:
        print(f'Unable to update config {name}. File not found at {path}')
    except Exception as e:
        print(f'Failed to update config {name}. Error: {e}')


