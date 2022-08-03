"""
This file is used to map a config name to the config filename it can be found in.
When a new config file is added to the configs directory its name and file should be added here.
"""


config_map = {
    'NUMBER_RESPONSES_RETAINED': 'number_responses_retained.ini',
    'REQUESTS_DIR': 'requests_directory.ini',
    'RESPONSES_DIR': 'responses_directory.ini',
    'SUPPRESS_OUTPUT': 'suppress_output.ini',
}

config_file_map = {
    'number_responses_retained.ini': 'NUMBER_RESPONSES_RETAINED',
    'requests_directory.ini': 'REQUESTS_DIR',
    'responses_directory.ini': 'RESPONSES_DIR',
    'suppress_output.ini': 'SUPPRESS_OUTPUT',
}


def get_config_filename(config: str):
    return config_map.get(config)

