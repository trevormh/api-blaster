from __future__ import annotations
from typing import Optional
from api_blaster.request.formatter.abstract_handler import AbstractHandler


class Handler(AbstractHandler):

    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return handler

    def next(self, request, request_str) -> Optional[str]:
        if self._next_handler:
            return self._next_handler.next(request, request_str)
        elif self._next_handler is None:
            return request_str
