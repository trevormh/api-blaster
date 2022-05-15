from api_blaster.cli.commands.command import Command
from api_blaster.request.formatter.formatter import Formatter
import json


class HttpRequest(Command):

    def __init__(self):
        self.url = ''
        self.headers = {}

    def __repr__(self):
        attrs = {}
        for attribute, value in self.__dict__.items():
            attrs[attribute] = value
        return json.dumps(attrs)

    def execute(self):
        fmt = Formatter(self).format()
        print(fmt)
