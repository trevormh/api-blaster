import sys, os, re

from api_blaster.request.builder.abstract_builder import AbstractBuilder
from api_blaster.request.http_request import HttpRequest
import json
from dotenv import load_dotenv


class RequestBuilder(AbstractBuilder):

    env_regex = "{{(.*?)}}(?!})"
    default_method = 'GET'

    def __init__(self, directory: str, filename: str):
        self.path = directory
        self.filename = filename
        self.request_config = self.load_json_config(f"{directory}/{filename}")
        self.request = HttpRequest()
        self._set_env_path()

    def _set_env_path(self):
        if os.path.isfile(f"{self.path}/.env"):
            load_dotenv(f"{self.path}/.env")
            self.env_loaded = True
        else:
            self.env_loaded = False

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
            try:
                item = item.replace("{{" + env + "}}", os.getenv(env))
            except Exception as e:
                # TODO implement better warning handling
                import warnings
                warning = '\33[33m'
                end = '\033[0m'
                warnings.warn(
                    f"{warning}.env file missing variable {env} used by request{end}",
                    RuntimeWarning, stacklevel=2, source=None)
        return item

    def find_env_var(self, s: str) -> list:
        return re.findall(rf"{self.env_regex}", s)

    def set_url(self):
        url = self.request_config['url']
        env_vars = self.find_env_var(url)
        if env_vars and self.env_loaded:
            url = self.apply_env_vars(url, env_vars)
        elif env_vars and not self.env_loaded:
            # TODO implement better warning handling
            import warnings
            warning = '\33[33m'
            end = '\033[0m'
            warnings.warn(f"{warning}Request contains env variables, but no .env file was found in the following directory at the following path: {self.path}{end}", RuntimeWarning, stacklevel=2, source=None)
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
        filename = self.filename
        self.request.name = filename.replace(".json", "")
