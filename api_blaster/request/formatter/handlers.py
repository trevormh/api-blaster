from api_blaster.request.formatter.handler import Handler
from typing import Any


class ProtocolHandler(Handler):
    def next(self, request: Any, request_str: str) -> Any:
        request_str = "http"
        return super().next(request, request_str)


class AuthHandler(Handler):
    def next(self, request: Any, request_str: str) -> Any:
        if "Authorization" in request.headers:
            request_str += self._auth_str(request)
        return super().next(request, request_str)

    def _auth_str(self, request: Any) -> str:
        auth = request.headers['Authorization'].rpartition(" ")
        type = auth[0]
        creds = auth[2]
        if type.lower() == "basic":
            return f" -a {creds}"
        elif type.lower() == "bearer":
            return f" -A bearer -a {creds}"


class MethodHandler(Handler):
    def next(self, request: Any, request_str: str) -> Any:
        request_str += self._method_str(request)
        return super().next(request, request_str)

    def _method_str(self, request: Any) -> str:
        return f" {request.headers['method']}"


class URLHandler(Handler):
    def next(self, request: Any, request_str: str) -> Any:
        request_str += self._url_str(request)
        return super().next(request, request_str)

    def _url_str(self, request: Any) -> str:
        return f" {request.url}"


class FormHandler(Handler):
    def next(self, request: Any, request_str: str) -> Any:
        return super().next(request, request_str)
