import os

from api_blaster.cli.commands.command import Command
import configparser
from typing import TYPE_CHECKING
from api_blaster.__main__ import REQUESTS_DIR, set_requests_dir

from api_blaster.cli.helpers import info, warn, critical

if TYPE_CHECKING:
    from api_blaster.cli.menu_builder import MenuBuilder


class SettingsCommand(Command):

    def __init__(self, setting: str):
        self.path = f"{os.path.dirname(os.path.realpath(__file__))}/settings"
        self.setting = setting
        self.config = configparser.ConfigParser()
        self.config_path = f"{self.path}/{self.setting}"


    def execute(self):
        # self.__read_config_file()
        if self.setting == 'update_requests_directory.ini':
            self.__update_requests_directory()
        else:
            return

    def __repr__(self):
        name = self.setting.rpartition(".")
        return name[0].replace("_", " ").title()

    def __read_config_file(self):
        try:
            self.config.read(self.config_path)
        except Exception as e:
            print(e)

    def get_config_value(self, config: dict):
        self.__read_config_file()
        try:
            section = config['section']
            setting = config['setting']
            return self.config[section][setting]
        except Exception as e:
            print(e)

    def update_config(self, new_config: dict) -> bool:
        try:
            with open(self.config_path, 'w') as configfile:
                section = new_config['section']
                setting = new_config['setting']
                self.config[section][setting] = new_config['value']
                self.config.write(configfile)
                return True
        except Exception as e:
            print(e)

    def __update_requests_directory(self):
        config = {'section': 'APP', 'setting': 'REQUESTS_DIRECTORY'}
        cur_config = self.get_config_value(config)
        info(f'Current request directory: {cur_config}')
        new_dir = input('Please enter new requests directory path (press enter to cancel): ')
        if new_dir:
            config['value'] = new_dir
            update_dir_var = set_requests_dir(new_dir)
            if update_dir_var and self.update_config(config):
                print('Request directory updated successfully')
            # update_config returns False if the directory does not exist
            # make the user enter a valid directory when this happens
            elif not update_dir_var:
                warn(f'{new_dir} is not a valid directory. Please choose another directory.')
                self.__update_requests_directory()
            else:
                critical('Error occurred, requests directory was not updated.')
