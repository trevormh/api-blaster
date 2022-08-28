import asyncio
from typing import Optional, Awaitable

import tornado.escape
import tornado.locks
import tornado.web
import os.path
from api_blaster.event import event

from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")

responses_dir = ''

class FileUpdateCheck(object):

    def __init__(self):
        self.cond = tornado.locks.Condition()
        self.refresh = False

    def get_status(self):
        return self.refresh

    def set_refresh_status(self, should_refresh: bool):
        self.refresh = should_refresh
        self.cond.notify_all()


file_check = FileUpdateCheck()


@event.on("request_completed")
def update_refresh_status():
    file_check.set_refresh_status(True)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", should_refresh='false')


class RefreshHandler(tornado.web.RequestHandler):

    async def post(self):
        refresh = file_check.get_status()
        while not refresh:
            self.wait_future = file_check.cond.wait()
            try:
                await self.wait_future
            except asyncio.CancelledError:
                return
            refresh = file_check.get_status()
        file_check.refresh = False
        if self.request.connection.stream.closed():
            return
        refresh = 'true' if refresh else 'false'
        self.write(dict(should_refresh=refresh))

    def on_connection_close(self):
        self.wait_future.cancel()


class MostRecentHandler(tornado.web.RequestHandler):

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        path = self.request.path
        if filename := self.get_filename(path):
            # self.write(dict(should_refresh='false', filename=filename))
            self.render("render.html", should_refresh='false', filename=filename)


    async def post(self):
        refresh = file_check.get_status()
        while not refresh:
            self.wait_future = file_check.cond.wait()
            try:
                await self.wait_future
            except asyncio.CancelledError:
                return
            refresh = file_check.get_status()
        file_check.refresh = False
        if self.request.connection.stream.closed():
            return
        refresh = 'true' if refresh else 'false'
        self.write(dict(should_refresh=refresh))

    def get_filename(self, file_path: str):
        if file_path:
            from pathlib import Path
            try:
                filename = file_path.rpartition("/")
                request_name = filename[2].split("request=")
                pattern = f'*request={request_name[1]}'
                path_dir = Path(responses_dir)
                latest = max(path_dir.glob(pattern), key=os.path.getctime)

                filename = str(latest).rpartition("/")
                return filename[2]
            except:
                print('here')
                return False
        else:
            return False


class RenderMostRecentHandler(tornado.web.RequestHandler):

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        path = self.request.path
        if path:
            from pathlib import Path
            try:
                filename = path.rpartition("/")
                request_name = filename[2].split("request=")
                pattern = f'*request={request_name[1]}'
                path_dir = Path(responses_dir)
                latest = max(path_dir.glob(pattern), key=os.path.getctime)
                self.write(get_file(latest))
            except:
                self.write(f'No requests found for {path}')
        else:
            self.write('No file specified in URL')


def get_file(filename):
    if not file_exists(filename):
        return f'Response {filename} not found'
    try:
        with open(os.path.join(responses_dir, filename), encoding="latin1") as file:
            return file.read()
    except Exception as e:  # TODO - better error handling
        return e


def file_exists(filename):
    if os.path.isfile(os.path.join(responses_dir, filename)):
        return True
    return False

async def main(dir):
    import logging
    hn = logging.NullHandler()
    hn.setLevel(logging.DEBUG)
    logging.getLogger("tornado.access").addHandler(hn)
    logging.getLogger("tornado.access").propagate = False
    logging.getLogger('tornado.access').disabled = True

    global responses_dir
    responses_dir = dir

    # Parses all options given on the command line
    parse_command_line()
    app = tornado.web.Application(
        [
            # (r"/", MainHandler),
            (r"/refesh", RefreshHandler),
            (r"/most_recent/.*", MostRecentHandler),
            (r"/render_most_recent/.*", RenderMostRecentHandler)
        ],
        cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=options.debug,
    )
    app.listen(options.port)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
