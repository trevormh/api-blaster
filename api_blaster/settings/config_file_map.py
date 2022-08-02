"""
This file is used to map a config name to the config filename it can be found in.
When a new config file is added to the configs directory its name and file should be added here.
"""


config_map = {
    'NUMBER_RESPONSES_RETAINED': 'number_responses_retained.ini',
    'REQUESTS_DIRECTORY': 'requests_directory.ini',
    'RESPONSES_DIRECTORY': 'responses_directory.ini',
    'SUPPRESS_OUTPUT': 'suppress_output.ini',
}


def get_config_filename(config: str):
    return config_map.get(config)

