import os
import time
from distutils.util import strtobool
from glob import glob
from typing import Any, List, Union
from api_blaster.request.formatter.handler import Handler
from api_blaster.settings.cfg import get_config


class ProtocolHandler(Handler):
    def next(self, request: Any, request_params: List[str]) -> list[str]:
        request_params.append("https")  # TODO make this dynamic based on request
        return super().next(request, request_params)


class FollowRedirects(Handler):
    def next(self, request: Any, request_params: List[str]) -> list[str]:
        request_params.append("--follow")  # TODO read this from settings
        return super().next(request, request_params)


class AuthHandler(Handler):
    def next(self, request: Any, request_params: List[str]) -> list[str]:
        if "Authorization" in request.headers:
            auth = self._auth_str(request)
            if auth:
                request_params.extend(auth)
        return super().next(request, request_params)

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


class HeadersHandler(Handler):
    def next(self, request: Any, request_params: List[str]) -> list[str]:
        for key, val in request.headers.items():
            if key.lower() == "authorization":
                auth = self._auth_str(request)
                if auth:
                    request_params.extend(auth)
            else:
                request_params.extend([f'{key}:{val}'])
        return super().next(request, request_params)

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
    def next(self, request: Any, request_params: List[str]) -> list[str]:
        if get_config('SUPPRESS_OUTPUT'):
            request_params.append("--quiet")
            print('Output Suppressed')
        else:
            request_params.append('--pretty=all')
        return super().next(request, request_params)


class SaveResponseHandler(Handler):

    def __init__(self, request):
        self.max_num_responses = int(get_config('NUMBER_RESPONSES_RETAINED'))
        self.responses_dir = get_config('RESPONSES_DIR')
        self.request = request

    def next(self, request: Any, request_params: List[str]) -> list[str]:
        if self.max_num_responses > 0:
            response_name = f'{time.time()}_request={request.name}.txt'
            response_path = os.path.join(self.responses_dir, response_name)
            request_params.append('--pretty=none')  # don't print color, encodings will be saved in response file
            request_params.append('--print=hb')  # print both response headers and body
            request_params.append('--output')
            request_params.append(response_path)
            self.request.event.emit("set_response_filepath", self.request, response_path)
            self.__handle_old_files()
        return super().next(request, request_params)

    def __handle_old_files(self, ):
        files = glob(f'{self.responses_dir}/*.txt')
        # add one to account for new response being saved
        num_files_to_remove = len(files) - self.max_num_responses + 1
        if num_files_to_remove > 0:
            files = self.__get_oldest_files(files, num_files_to_remove)
            self.__remove_files(files)

    def __get_oldest_files(self, files, num_files_to_remove):
        files_to_remove = []
        files_date_ascending = sorted(files, key=os.path.getctime, reverse=False)
        for file in files_date_ascending:
            if num_files_to_remove > 0:
                files_to_remove.append(file)
                num_files_to_remove -= 1
            else:
                break
        return files_to_remove

    def __remove_files(self, files):
        for file in files:
            os.remove(file)


class MethodHandler(Handler):
    def next(self, request: Any, request_params: List[str]) -> list[str]:
        request_params.append(request.headers['method'])
        return super().next(request, request_params)


class URLHandler(Handler):
    def next(self, request: Any, request_params: List[str]) -> list[str]:
        request_params.append(request.url)
        return super().next(request, request_params)


class FormHandler(Handler):
    def next(self, request: Any, request_params: List[str]) -> list[str]:
        return super().next(request, request_params)
