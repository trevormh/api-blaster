import asyncio
import tornado.escape
import tornado.locks
import tornado.web
from api_blaster.event import event


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
