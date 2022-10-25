import os

from api_blaster.__main__ import is_port_available
from api_blaster.cli.commands.command import Command
from api_blaster.event import event
import configparser
from typing import TYPE_CHECKING
from api_blaster.settings.cfg import get_config, update_config, get_config_info
from api_blaster.cli.helpers import info, alert
from api_blaster.settings.config_file_map import ConfigFileName, ConfigName
from api_blaster_server.main import restart_server

if TYPE_CHECKING:
    pass


class SettingsCommand(Command):

    def __init__(self, filename: str):
        self.filename = filename
        self.config_name = ConfigFileName(filename).name
        self.config = configparser.ConfigParser()
        self.config_path = os.path.join(get_config('SETTINGS_DIR'), self.filename)

    def execute(self):
        if self.config_name == ConfigName.NUMBER_RESPONSES_RETAINED.value:
            self.__update_number_responses()
        elif self.config_name == ConfigName.REQUESTS_DIR.value:
            self.__update_requests_directory()
        elif self.config_name == ConfigName.RESPONSES_DIR.value:
            self.__update_responses_directory()
        elif self.config_name == ConfigName.SUPPRESS_OUTPUT.value:
            self.__update_suppress_output()
        elif self.config_name == ConfigName.SERVER_STARTUP.value:
            self.__update_server_startup()
        elif self.config_name == ConfigName.PORT_NUMBER.value:
            self.__update_port_number()
        else:
            return

    def __repr__(self):
        name = self.filename.rpartition(".")
        return name[0].replace("_", " ").title()

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
        info(f'Current suppress output value: {bool(get_config(self.config_name))}')
        info(f'About: {get_config_info(self.config_name)}')
        suppress = input('Suppress output? (True or False): ').capitalize()
        if suppress in ['True', 'False']:
            if update_config(self.config_path, self.config_name, value=suppress):
                event.emit("reload_httpie")
                alert('Suppress output setting updated successfully')
            else:
                alert(f'Failed to update config {self.config_name}')
        elif suppress != '':
            alert(f"{suppress} is not a valid selection. Please choose True or False")
            self.__update_suppress_output()

    def __update_server_startup(self):
        info(f'Current server startup value: {bool(get_config(self.config_name))}')
        info(f'About: {get_config_info(self.config_name)}')
        startup = input('Start server when API blaster starts? (True or False): ').capitalize()
        if startup in ['True', 'False']:
            if update_config(self.config_path, self.config_name, value=startup):
                alert('Server startup updated successfully')
            else:
                alert(f'Failed to update config {self.config_name}')
        elif startup != '':
            alert(f"{startup} is not a valid selection. Please choose True or False")
            self.__update_server_startup()

    def __update_port_number(self):
        info(f'Current port number: {get_config(self.config_name)}')
        port_number = input('Port number: ')
        if port_number.isdigit():
            if is_port_available(int(port_number)):
                if update_config(self.config_path, self.config_name, value=port_number):
                    alert('Port number updated successfully')
                    # TODO - event emit port changed. restart server with new port num
                    # event.emit("port_number_changed")
                    try:
                        restart_server()
                    except Exception as e:
                        print(e)
                else:
                    alert(f'Failed to update config {self.config_name}')
            else:
                alert(f"{port_number} is currently in use. Please choose a different port number")
                self.__update_port_number()
        elif port_number != '':
            alert(f"{port_number} is not a valid selection. Please choose a number.")
            self.__update_port_number()
