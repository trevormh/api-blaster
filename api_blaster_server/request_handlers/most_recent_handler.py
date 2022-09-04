import asyncio
from typing import Optional, Awaitable
import tornado.web
import os.path


class MostRecentHandler(tornado.web.RequestHandler):

    def initialize(self, responses_dir: str):
        self.responses_dir = responses_dir

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        path = self.request.path
        filename, extension = self.get_most_recent_filename(path)
        if filename:
            if extension == ".json":
                self.render("render_json.html", should_refresh='false', filename=filename)
            else:
                self.render("render.html", should_refresh='false', filename=filename)


    # async def post(self):
    #     refresh = file_check.get_status()
    #     while not refresh:
    #         self.wait_future = file_check.cond.wait()
    #         try:
    #             await self.wait_future
    #         except asyncio.CancelledError:
    #             return
    #         refresh = file_check.get_status()
    #     file_check.refresh = False
    #     if self.request.connection.stream.closed():
    #         return
    #     refresh = 'true' if refresh else 'false'
    #     self.write(dict(should_refresh=refresh))

    # Saved response filenames all have the request name as part of the filename
    # in the form of /path/to/timestamp_request=request-name.extension
    # Ex /home/responses/1662087575.251782_request=test1-get.json
    def get_most_recent_filename(self, file_path: str):
        if file_path:
            from pathlib import Path
            try:
                p = Path(file_path)
                filename = p.name
                # print(f'filename: {filename}')
                # split at "request=" to get the request name
                request_name = filename.split("request=")
                pattern = f'*request={request_name[1]}'
                path_dir = Path(self.responses_dir)
                # search the responses directory for the most recently created file
                # having the request_name
                latest = max(path_dir.glob(pattern), key=os.path.getctime)
                latest_path = Path(latest)
                return latest_path.name, latest_path.suffix
            except Exception as e:
                print(e)
                return False
        else:
            return False