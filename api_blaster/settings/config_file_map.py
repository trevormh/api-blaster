"""
This file is used to map a config name to the config filename it can be found in.
When a new config file is added to the configs directory its name and file should be added here.
"""
from enum import Enum, unique


@unique
class ConfigName(Enum):
    NUMBER_RESPONSES_RETAINED = 'NUMBER_RESPONSES_RETAINED'
    REQUESTS_DIR = 'REQUESTS_DIR'
    RESPONSES_DIR = 'RESPONSES_DIR'
    SERVER_STARTUP = 'SERVER_STARTUP'
    SETTINGS_DIR = 'SETTINGS_DIR'
    SUPPRESS_OUTPUT = 'SUPPRESS_OUTPUT'
    PORT_NUMBER = 'PORT_NUMBER'


@unique
class ConfigFileName(Enum):
    NUMBER_RESPONSES_RETAINED = 'number_responses_retained.ini'
    REQUESTS_DIR = 'requests_directory.ini'
    RESPONSES_DIR = 'responses_directory.ini'
    SERVER_STARTUP = 'server_startup.ini'
    SUPPRESS_OUTPUT = 'suppress_output.ini'
    PORT_NUMBER = 'port_number.ini'
