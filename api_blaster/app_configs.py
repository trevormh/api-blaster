import configparser
import os

class AppConfigs:

    __configs = {}

    def __init__(self, root_dir: str = None):
        self.__dict__ = self.__configs
        if not len(self.__dict__):
            self.__dict__['ROOT_DIR'] = root_dir
            self.__dict__['SETTINGS_DIR'] = f"{os.path.dirname(os.path.realpath(__file__))}/cli/commands/settings"
            self.config_parser = configparser.ConfigParser()
            self.load_cfg_files()

    def load_cfg_files(self):
        self.__load_requests_dir()
        # self.__load_responses_dir()
        # self.__load_num_responses_saved()

    def __load_requests_dir(self):
        try:
            # os.path.join(data_dir, file_name)
            self.config_parser.read(self.__dict__['SETTINGS_DIR'] + '/requests_directory.ini')
            requests_dir = self.config_parser['APP']['REQUESTS_DIR']
            self.set_config('REQUESTS_DIR', requests_dir)
        except FileNotFoundError:
            print('requests_directory.ini file not found, using default requests directory')
            print(f"requests directory path: {self.__dict__['REQUESTS_DIR']}")
        except Exception as exp:
            breakpoint()
            print('Failed to initialize requests dir')

    def __load_responses_dir(self):
        pass  # TODO

    def __load_num_responses_saved(self):
        pass  # TODO

    def get_config(self, config_name: str):
        return self.__dict__[config_name]

    def set_config(self, config_name: str, value: any):
        self.__dict__[config_name] = value
        return True

    # def update_config(self, config_name: str, value: any):
    #     pass
