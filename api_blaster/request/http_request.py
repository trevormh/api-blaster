import os.path
from urllib.parse import urlsplit, urlunsplit

from api_blaster.cli.commands.command import Command
from api_blaster.request.formatter.formatter import Formatter
import json
from pymitter import EventEmitter
import httpie.core
from importlib import reload


class HttpRequest(Command):

    event = EventEmitter()

    def __init__(self):
        self.url = ''
        self.headers = {}
        self.response_file = ''
        self.reload_httpie = False

    def __repr__(self):
        attrs = {}
        for attribute, value in self.__dict__.items():
            attrs[attribute] = value
        return json.dumps(attrs)

    def execute(self):
        # breakpoint()
        cmd = Formatter(self).format()
        # breakpoint()
        httpie.core.main(cmd)  # TODO, implement check to see if reload is needed for when suppress setting was changed from quiet to all
        reload(httpie.core)
        cleanup_response(self.response_file, self.url)
        response_name = self.response_file.rpartition("/")[2]
        url = f'http://localhost:8000/response/{response_name}'  # TODO get host and port from settings
        print(f'View response: {url}')  # TODO - make this less sloppy

    @event.on("set_response_filepath")
    def set_response_filepath(self, filepath):
        self.response_file = filepath

    # TODO - implement!
    @event.on("reload_httpie")
    def reload_httpie(self):
        print("Reload Httpie")
        self.reload_httpie = True


def cleanup_response(response_file: str,  url: str):
    if not response_file or not os.path.isfile(response_file):
        print(f"invalid response file provided: {response_file}")
    url = get_base_url(url)
    tmp_file = create_tmp_response_file(response_file, url)
    update_response_file(response_file, tmp_file)
    os.remove(tmp_file)


def get_base_url(url: str):
    split = urlsplit(url)
    url = split.netloc
    if not split.scheme:
        return url
    return f'{split.scheme}://{url}/'


def create_tmp_response_file(response_file: str, url: str) -> str:
    file_split = response_file.rpartition('/')
    path = file_split[0]
    filename = file_split[2]
    tmp_filename = f"tmp_{filename}"  # create new file prefixed w/ "tmp"
    with open(tmp_file_path := os.path.join(path, tmp_filename), "w+") as tmp_file:
        for line in read_file(response_file):
            line = line.replace('href="/', f'href="{url}')
            line = line.replace('src="/', f'src="{url}')
            line = line.replace("src='/", f'src="{url}')
            line = line.replace('content="/', f'content="{url}')
            line = line.replace('background:url(/', f'background:url({url}')
            tmp_file.write(line)
    return tmp_file_path


def update_response_file(response_file, tmp_response_file):
    with open(response_file, "w+", encoding="latin1") as response_file:
        for line in read_file(tmp_response_file):
            response_file.write(line)


def read_file(file: str):
    with open(file, 'r', encoding="latin1") as file:
        for line in file:
            yield line
