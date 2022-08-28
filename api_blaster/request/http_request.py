from api_blaster.cli.commands.command import Command
from api_blaster.request.cleanup import cleanup_response
from api_blaster.request.formatter.formatter import Formatter
import json
from api_blaster.request.make_request import make_request
from api_blaster.event import event


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
        self.event.emit("request_completed")
        url = f'http://localhost:8000/most_recent/{response_name}'  # TODO get host and port from settings
        print(f'View most recent: {url}')  # TODO - make this less sloppy
        url = f'http://localhost:8000/response_by_filename/{response_name}'
        print(f'View response by filename: {url}')  # TODO - make this less sloppy

    @event.on("set_response_filepath")
    def set_response_filepath(self, filepath):
        self.response_file = filepath
