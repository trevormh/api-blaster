import sys, os, re

from api_blaster.request.builder.abstract_builder import AbstractBuilder
from api_blaster.request.http_request import HttpRequest
import json


class RequestBuilder(AbstractBuilder):
    env_regex = "{{(.*?)}}(?!})"
    default_method = 'GET'

    def __init__(self, request_file_path: str):
        self.path = request_file_path
        self.request_config = self.load_json_config(request_file_path)
        self._load_env_configs()
        self.request = HttpRequest()

    def _load_env_configs(self):
        """
        Load any environment variables and credentials into the environment_config instance property
        """
        self.environment_config = {}
        dir = self.path.rpartition("/")[0]
        if os.path.isfile(f"{dir}/environment.json"):
            env_path = f"{dir}/environment.json"
            self.environment_config = self.load_json_config(env_path)
        if os.path.isfile(f"{dir}/credentials.json"):
            env_path = f"{dir}/credentials.json"
            self.environment_config.update(self.load_json_config(env_path))

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
        self.set_name()
        self.set_headers()
        return self.request

    def apply_env_vars(self, item: str, env_vars: list[str]) -> str:
        for env in env_vars:
            item = item.replace("{{" + env + "}}", self.environment_config[env])
        return item

    def find_env_var(self, s: str) -> list:
        return re.findall(rf"{self.env_regex}", s)

    def set_url(self):
        url = self.request_config['url']
        env_vars = self.find_env_var(url)
        if env_vars:
            url = self.apply_env_vars(url, env_vars)
        self.request.url = url

    def set_headers(self):
        if 'headers' in self.request_config:
            self.request.headers = {}
            for header, val in self.request_config['headers'].items():
                env_vars = self.find_env_var(val)
                if env_vars:
                    val = self.apply_env_vars(val, env_vars)
                self.request.headers[header] = val
        # if no method is set use GET by default
        if "method" not in self.request.headers:
            self.request.headers["method"] = "GET"

    def set_name(self):
        filename = self.path.rpartition("/")[2]
        self.request.name = filename.replace(".json", "")
