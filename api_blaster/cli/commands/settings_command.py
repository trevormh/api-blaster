import os

from api_blaster.cli.commands.command import Command
import configparser
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from api_blaster.cli.menu_builder import MenuBuilder


class SettingsCommand(Command):

    def __init__(self, setting: str):
        self.path = f"{os.path.dirname(os.path.realpath(__file__))}/settings"
        self.setting = setting
        self.config = configparser.ConfigParser()
        self.config_path = f"{self.path}/{self.setting}"

    def read_file(self):
        self.__read_config()
        print(self.config['APP']['REQUESTS_DIRECTORY'])

    def execute(self):
        self.__read_config()
        self.read_file()
        if self.setting == 'update_requests_directory.ini':
            self.__update_requests_directory()

    def __repr__(self):
        name = self.setting.rpartition(".")
        return name[0].replace("_"," ").title()

    def __read_config(self):
        try:
            self.config.read(self.config_path)
        except Exception as e:
            print(e)


    def __update_requests_directory(self):
        # requests_directory = /Users/trevorholloway/software_dev/api_blaster_requests
        self.config['APP']['REQUESTS_DIRECTORY'] = '12345'
        with open(self.config_path, 'w') as configfile:
            self.config.write(configfile)
