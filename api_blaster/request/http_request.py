from api_blaster.cli.commands.command import Command
from api_blaster.request.formatter.formatter import Formatter
import json
# from httpie.core import main as httpie_main  # type: ignore
import httpie.core
from importlib import reload

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
        # breakpoint()
        cmd = Formatter(self).format()
        httpie.core.main(cmd)  # TODO, implement check to see if reload is needed for when suppress setting was changed from quiet to all
        reload(httpie.core)
