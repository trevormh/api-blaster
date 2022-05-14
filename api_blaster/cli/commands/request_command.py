from api_blaster.cli.commands.command import Command
from typing import Union, TYPE_CHECKING

from api_blaster.request.builder.request_builder import RequestBuilder

if TYPE_CHECKING:
    from api_blaster.cli.menu_builder import MenuBuilder


class RequestCommand(Command):

    def __init__(self, menu: 'MenuBuilder', request_path, environment_path: Union[str, None]):
        self.request_path = request_path
        self.menu = menu
        self.environment_path = environment_path

    def execute(self):
        request = RequestBuilder(self.request_path, self.environment_path).build()
        print(request)

    def __repr__(self):
        return self.request_path.rpartition("/")[2]