from api_blaster.request.formatter.handler import Handler
import api_blaster.request.formatter.handlers as handlers
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from api_blaster.request.http_request import HttpRequest


class Formatter:

    # TODO implement chain of command to responsibility to make sure each item in sequence of httpie commands are in order
    # https://refactoring.guru/design-patterns/chain-of-responsibility
    # https://refactoring.guru/design-patterns/chain-of-responsibility/python/example
    # https://httpie.io/docs/cli/examples
    def __init__(self, request: 'HttpRequest'):
        self.request = request
        self.handlers = self._set_handlers()

    def _set_handlers(self) -> Handler:
        protocol = handlers.ProtocolHandler()
        auth = handlers.AuthHandler()
        form = handlers.FormHandler()
        method = handlers.MethodHandler()
        url = handlers.URLHandler()
        protocol.set_next(auth).set_next(form).set_next(method).set_next(url)
        return protocol

    def format(self) -> str:
        return self.handlers.next(self.request, '')