import json


class HttpRequest:

    def __init__(self):
        self.url = ''
        self.method = ''
        self.headers = {}

    def execute(self):
        pass

    def __repr__(self):
        attrs = {}
        for attribute, value in self.__dict__.items():
            attrs[attribute] = value
        return json.dumps(attrs)