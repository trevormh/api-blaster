import os

from api_blaster.cli.commands.command import Command
import configparser
from typing import TYPE_CHECKING
from api_blaster.__main__ import REQUESTS_DIR, set_requests_dir

from api_blaster.cli.helpers import info, warn, critical, alert

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
        if self.setting == 'requests_directory.ini':
            self.__update_requests_directory()
        elif self.setting == 'responses_directory.ini':
            self.__update_responses_directory()
        elif self.setting == 'number_responses_retained.ini':
            self.__update_number_responses()
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
        if new_dir := input('Please enter new requests directory path (press enter to cancel): '):
            config['value'] = new_dir
            if update_dir_var := set_requests_dir(new_dir) and self.update_config(config):
                print('Request directory updated successfully')
            # update_config returns False if the directory does not exist
            # make the user enter a valid directory when this happens
            elif not update_dir_var:
                alert(f'{new_dir} does not exist. Please choose another directory.')
                self.__update_requests_directory()
            else:
                critical('Error occurred, requests directory was not updated.')

    def __update_responses_directory(self):
        config = {'section': 'APP', 'setting': 'RESPONSES_DIRECTORY'}
        cur_config = self.get_config_value(config)
        info(f'Current responses directory: {cur_config}')
        if new_dir := input('Please enter new responses directory path (press enter to cancel): '):
            config['value'] = new_dir
            if update_dir_var := set_requests_dir(new_dir) and self.update_config(config):
                print('Responses directory updated successfully')
            # update_config returns False if the directory does not exist
            # make the user enter a valid directory when this happens
            elif not update_dir_var:
                alert(f'{new_dir} does not exist. Please choose another directory.')
                self.__update_responses_directory()
            else:
                critical('Error occurred, responses directory was not updated.')

    def __update_number_responses(self):
        value_config = {'section': 'APP', 'setting': 'NUMBER_RESPONSES_RETAINED'}
        cur_config_value = self.get_config_value(value_config)
        info(f'Current number of responses retained: {cur_config_value}')

        info_config = {'section': 'APP', 'setting': 'INFO'}
        config_info = self.get_config_value(info_config)
        info(f'About: {config_info}')
        if new_num := input('Please enter number of responses to retain (press enter to cancel): '):
            value_config['value'] = new_num
            if new_num_valid := new_num.isdigit() and self.update_config(value_config):
                alert('Number of retained responses updated successfully')
            elif not new_num_valid:
                alert('Please enter a number')
                self.__update_number_responses()
            else:
                critical('Error occurred, number of retained responses was not updated.')