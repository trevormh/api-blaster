import os
import sys

from api_blaster.cli.commands.command import Command
import configparser
from typing import TYPE_CHECKING
from api_blaster.settings.cfg import set_app_config, get_config, update_config, get_config_info

from api_blaster.cli.helpers import info, critical, alert
from api_blaster.settings.config_file_map import config_map, config_file_map

if TYPE_CHECKING:
    pass


class SettingsCommand(Command):

    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config_name = config_file_map.get(config_file)
        self.config = configparser.ConfigParser()
        self.config_path = os.path.join(get_config('SETTINGS_DIR'), self.config_file)

    def execute(self):
        if self.config_name == 'REQUESTS_DIR':
            self.__update_requests_directory()
        elif self.config_name == 'RESPONSES_DIR':
            self.__update_responses_directory()
        elif self.config_name == 'NUMBER_RESPONSES_RETAINED':
            self.__update_number_responses()
        elif self.config_name == 'SUPPRESS_OUTPUT':
            self.__update_suppress_output()
        else:
            return

    def __repr__(self):
        name = self.config_file.rpartition(".")
        return name[0].replace("_", " ").title()

    def __read_config_file(self):
        try:
            self.config.read(self.config_path)
        except Exception as e:
            print(e)

    def __update_requests_directory(self):
        info(f'Current request directory: {get_config(self.config_name)}')
        if new_dir := input('Please enter new requests directory path (press enter to cancel): '):
            if os.path.isdir(new_dir):
                if update_config(self.config_path, self.config_name, value=new_dir):
                    print('Request directory updated successfully')
                else:
                    alert(f'Failed to update config {self.config_name}')
            else:
                alert(f'{new_dir} does not exist. Please choose another directory.')
                self.__update_requests_directory()

    def __update_responses_directory(self):
        info(f'Current responses directory: {get_config(self.config_name)}')
        if new_dir := input('Please enter new responses directory path (press enter to cancel): '):
            if os.path.isdir(new_dir):
                if update_config(self.config_path, self.config_name, value=new_dir):
                    print('Responses directory updated successfully')
                else:
                    alert(f'Failed to update config {self.config_name}')
            else:
                alert(f'{new_dir} does not exist. Please choose another directory.')
                self.__update_responses_directory()

    def __update_number_responses(self):
        info(f'Current number of responses retained: {get_config(self.config_name)}')
        info(f'About: {get_config_info(self.config_name)}')
        if new_num := input('Please enter number of responses to retain (press enter to cancel): '):
            if new_num.isdigit():
                if update_config(self.config_path, self.config_name, value=new_num):
                    print('Number of retained responses updated successfully')
                else:
                    alert(f'Failed to update config {self.config_name}')
            else:
                alert('Please enter a number')
                self.__update_number_responses()

    def __update_suppress_output(self):
        info(f'Current suppress output value: {get_config(self.config_name)}')
        info(f'About: {get_config_info(self.config_name)}')

        suppress = input('Suppress output? (True or False): ').capitalize()
        if suppress in ['True', 'False']:
            if update_config(self.config_path, self.config_name, value=suppress):
                alert('Suppress output setting updated successfully')
            else:
                alert(f'Failed to update config {self.config_name}')
        elif suppress != '':
            alert(f"{suppress} is not a valid selection. Please choose True or False")
            self.__update_suppress_output()
