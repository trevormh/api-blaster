from api_blaster.cli.commands.command import Command
from api_blaster.request.cleanup import cleanup_response
from api_blaster.request.formatter.formatter import Formatter
import json
from api_blaster.request.make_request import event, make_request


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
        cleanup_response(self.response_file, self.url)
        response_name = self.response_file.rpartition("/")[2]
        url = f'http://localhost:8000/response/{response_name}'  # TODO get host and port from settings
        print(f'View response: {url}')  # TODO - make this less sloppy

    @event.on("set_response_filepath")
    def set_response_filepath(self, filepath):
        print("set_response_filepath called")
        self.response_file = filepath
