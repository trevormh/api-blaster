from api_blaster.request.formatter.handler import Handler
import api_blaster.request.formatter.handlers as handlers
from typing import TYPE_CHECKING, List


if TYPE_CHECKING:
    from api_blaster.request.http_request import HttpRequest


class Formatter:

    def __init__(self, request: 'HttpRequest'):
        self.request = request
        self.handlers = self._set_handlers()

    def _set_handlers(self) -> Handler:
        protocol = handlers.ProtocolHandler()
        follow_redirects = handlers.FollowRedirects()
        # auth = handlers.AuthHandler()
        headers = handlers.HeadersHandler()
        form = handlers.FormHandler()
        # method = handlers.MethodHandler()
        url = handlers.URLHandler()
        suppress = handlers.SuppressOutputHandler()
        save_response = handlers.SaveResponseHandler(self.request)

        protocol \
            .set_next(follow_redirects) \
            .set_next(url) \
            .set_next(form) \
            .set_next(headers) \
            .set_next(suppress) \
            .set_next(save_response)

        return protocol

    def format(self) -> List[str]:
        return self.handlers.next(self.request, [])
