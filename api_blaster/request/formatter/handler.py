from __future__ import annotations
from typing import TYPE_CHECKING, List, Callable, Union
from api_blaster.request.formatter.abstract_handler import AbstractHandler

if TYPE_CHECKING:
    from api_blaster.request.http_request import HttpRequest


class Handler(AbstractHandler):
    _next_handler: Union[None, Handler] = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return handler

    def next(self, request: 'HttpRequest', req_list: List[str]) -> List[str]:
        if self._next_handler:
            return self._next_handler.next(request, req_list)
        else:
            return req_list
