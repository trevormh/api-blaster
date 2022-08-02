import configparser, os

app_configs = {}


def initialize_configs(root_dir: str):
    app_configs['ROOT_DIR'] = root_dir
    app_configs['SETTINGS_DIR'] = os.path.join(root_dir, 'api_blaster', 'cli', 'commands', 'settings')
    __load_config_files()


def __load_config_files():
    config = configparser.ConfigParser()
    __load_config(config, 'REQUESTS_DIR', 'requests_directory.ini')
    __load_config(config, 'SUPPRESS_OUTPUT', 'suppress_output.ini')


def __load_config(config_parser, config_name: str, config_filename: str):
    path = os.path.join(app_configs['SETTINGS_DIR'], config_filename)
    try:
        if not os.path.isfile(path):
            raise FileNotFoundError
        config_parser.read(path)
        requests_dir = config_parser['APP'][config_name]
        set_config(config_name, requests_dir)
    except FileNotFoundError:
        print(f'File not found: {path}')
    except Exception as exp:
        print(exp)
        print('Failed to initialize requests dir')


def set_config(config_name: str, value: any):
    app_configs[config_name] = value
    return True


def get_config(config_name: str):
    return app_configs.get(config_name)
