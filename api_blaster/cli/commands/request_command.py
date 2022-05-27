from api_blaster.cli.commands.command import Command
from typing import Union, TYPE_CHECKING

from api_blaster.request.builder.request_builder import RequestBuilder

if TYPE_CHECKING:
    from api_blaster.cli.menu_builder import MenuBuilder


class RequestCommand(Command):

    def __init__(self, menu: 'MenuBuilder', directory: str, filename: str):
        self.directory = directory
        self.filename = filename
        self.menu = menu

    def execute(self):
        request = RequestBuilder(self.directory, self.filename).build()
        request.execute()

    def __repr__(self):
        return self.filename
