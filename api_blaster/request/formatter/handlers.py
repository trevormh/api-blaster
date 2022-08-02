from api_blaster.cfg import get_config
from api_blaster.request.formatter.handler import Handler
from typing import Any, List, Callable, Union
from distutils.util import strtobool


class ProtocolHandler(Handler):
    def next(self, request: Any, req_list: List[str]) -> list[str]:
        req_list.append("http")
        return super().next(request, req_list)


class AuthHandler(Handler):
    def next(self, request: Any, req_list: List[str]) -> list[str]:
        if "Authorization" in request.headers:
            auth = self._auth_str(request)
            if auth:
                req_list.extend(auth)
        return super().next(request, req_list)

    def _auth_str(self, request: Any) -> Union[List[str], None]:
        auth = request.headers['Authorization'].rpartition(" ")
        type = auth[0]
        creds = auth[2]
        if type.lower() == "basic":
            return ["-a", creds]
        elif type.lower() == "bearer":
            return ["-A", "bearer", "-a", creds]
        else:
            return None


class SuppressOutputHandler(Handler):
    def next(self, request: Any, req_list: List[str]) -> list[str]:
        if strtobool(get_config('SUPPRESS_OUTPUT')):
            req_list.append("--quiet")
            print('Output Suppressed')
        else:
            req_list.append('--pretty=all')
        return super().next(request, req_list)


class MethodHandler(Handler):
    def next(self, request: Any, req_list: List[str]) -> list[str]:
        req_list.append(request.headers['method'])
        return super().next(request, req_list)


class URLHandler(Handler):
    def next(self, request: Any, req_list: List[str]) -> list[str]:
        req_list.append(request.url)
        return super().next(request, req_list)


class FormHandler(Handler):
    def next(self, request: Any, req_list: List[str]) -> list[str]:
        return super().next(request, req_list)
