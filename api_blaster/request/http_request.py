from api_blaster.cli.commands.command import Command
from api_blaster.request.cleanup import extract_response_body_and_meta
from api_blaster.request.formatter.formatter import Formatter
import json
from api_blaster.request.make_request import make_request
from api_blaster.event import event
from api_blaster.settings.cfg import get_config
from api_blaster.settings.config_file_map import ConfigName
from api_blaster_server.request_handlers.refresh_handler import update_refresh_status


class HttpRequest(Command):

    def __init__(self):
        self.url = ''
        self.headers = {}
        self.response_file = ''
        self.reload_httpie = False
        self.event = event

    def __repr__(self):
        attrs = {}
        for attribute, value in self.__dict__.items():
            attrs[attribute] = value
        return json.dumps(attrs)

    def execute(self):
        cmd = Formatter(self).format()
        make_request(cmd)
        request_name = extract_response_body_and_meta(self.response_file, self.url)
        port_number = get_config(ConfigName.PORT_NUMBER.value)
        url = f'http://localhost:{port_number}/most_recent/{request_name}'  # TODO get host and port from settings
        print(f'View most recent: {url}')  # TODO - make this less sloppy
        url = f'http://localhost:{port_number}/response_by_filename/{request_name}'
        print(f'View response by filename: {url}')  # TODO - make this less sloppy
        self.event.emit("request_completed", request_name)
        # update_refresh_status(request_name)
        # print('done!')

    @event.on("set_response_filepath")
    def set_response_filepath(self, filepath):
        self.response_file = filepath
