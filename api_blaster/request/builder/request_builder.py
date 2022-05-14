import sys
import re

from api_blaster.request.builder.abstract_builder import AbstractBuilder
from api_blaster.request.builder.http_request import HttpRequest
import json


class RequestBuilder(AbstractBuilder):
    env_regex = "{{(.*?)}}(?!})"
    default_method = 'GET'

    def __init__(self, request_file_path: str, env_path: str):
        self.path = request_file_path
        self.request_config = self.load_json_config(request_file_path)
        self.env_config = self.load_json_config(env_path)
        self.request = HttpRequest()

    def load_json_config(self, path: str):
        try:
            with open(path) as f:
                return json.load(f)
        except IOError as e:
            print(e)
        except:
            print(f"Unexpected error attempting to read {path}: {sys.exc_info()[0]}")

    def build(self) -> HttpRequest:
        self.set_url()
        self.set_method()
        self.set_name()
        self.set_headers()
        return self.request

    def apply_env_vars(self, item: str, env_vars: list[str]) -> str:
        for env in env_vars:
            item = item.replace("{{" + env + "}}", self.env_config[env])
        return item

    def find_env_var(self, s: str) -> list:
        return re.findall(rf"{self.env_regex}", s)

    def set_url(self):
        url = self.request_config['url']
        env_vars = self.find_env_var(url)
        if env_vars:
            url = self.apply_env_vars(url, env_vars)
        self.request.url = url

    def set_method(self):
        if 'method' in self.request_config:
            self.request.method = self.request_config['method']
        else:
            self.request.method = self.default_method

    def set_headers(self):
        if 'headers' in self.request_config:
            self.request.headers = {}
            for header in self.request_config['headers']:
                env_vars = self.find_env_var(header)
                if env_vars:
                    header = self.apply_env_vars(header, env_vars)
                self.request.headers[header] = header

    def set_name(self):
        filename = self.path.rpartition("/")[2]
        self.request.name = filename.replace(".json", "")
