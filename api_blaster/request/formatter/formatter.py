from api_blaster.request.formatter.handler import Handler
import api_blaster.request.formatter.handlers as handlers
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from api_blaster.request.http_request import HttpRequest


class Formatter:

    def __init__(self, request: 'HttpRequest'):
        self.request = request
        self.handlers = self._set_handlers()

    def _set_handlers(self) -> Handler:
        protocol = handlers.ProtocolHandler()
        auth = handlers.AuthHandler()
        form = handlers.FormHandler()
        method = handlers.MethodHandler()
        url = handlers.URLHandler()
        protocol\
            .set_next(auth)\
            .set_next(form)\
            .set_next(method)\
            .set_next(url)
        return protocol

    def format(self) -> list[str]:
        return self.handlers.next(self.request, [])