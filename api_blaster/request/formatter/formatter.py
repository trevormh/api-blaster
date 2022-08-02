from api_blaster.cfg import get_config
from api_blaster.request.formatter.handler import Handler
import api_blaster.request.formatter.handlers as handlers
from typing import TYPE_CHECKING, Optional, List

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
        suppress = handlers.SuppressOutputHandler()

        protocol \
            .set_next(auth) \
            .set_next(form) \
            .set_next(method) \
            .set_next(url) \
            .set_next(suppress)

        # if get_config('SUPPRESS_OUTPUT'):
        #     suppress = handlers.SuppressOutputHandler()
        #     protocol.set_next(suppress)

        return protocol

    def format(self) -> List[str]:
        return self.handlers.next(self.request, [])
