
from typing import Optional, Awaitable
import tornado.web
from api_blaster_server.file_helpers import get_file


class ContentHandler(tornado.web.RequestHandler):

    def initialize(self, responses_dir: str):
        self.responses_dir = responses_dir

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        path = self.request.path
        if path:
            from pathlib import Path
            try:
                p = Path(path)
                filename = p.name
                file = get_file(self.responses_dir, filename)
                self.write(file)
            except Exception as e:
                self.write(f'No requests found for {path}')
        else:
            self.write('No file specified in URL')
