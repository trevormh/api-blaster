import asyncio
import tornado.escape
import tornado.locks
import tornado.web
from tornado import ioloop

from api_blaster.event import event


class FileUpdateCheck(object):

    def __init__(self):
        self.request_name = ''
        self.cond = tornado.locks.Condition()
        self.refresh = False

    def get_status(self, name) -> bool:
        # prevent refreshing other browser tabs for different requests
        if name == self.request_name and self.refresh:
            return True
        else:
            return False

    def set_refresh_status(self, should_refresh: bool, request_name: str) -> None:
        self.refresh = should_refresh
        self.request_name = request_name
        self.cond.notify_all()


file_check = FileUpdateCheck()



def this_is_a_hack():
    pass


scheduler = ioloop.PeriodicCallback(this_is_a_hack, 500)


def loop_check():
    if not scheduler.is_running():
        scheduler.start()


@event.on("request_completed")
def update_refresh_status(response_name: str) -> None:
    file_check.set_refresh_status(True, get_request_name(response_name))


def get_request_name(response_name: str) -> str:
    # response_name will be in the format of 'timestamp_request=request_name'
    # something like 1666918520.93619_request=test2-get.json
    request = response_name.rpartition('=')
    return request[2]


class RefreshHandler(tornado.web.RequestHandler):

    async def post(self) -> None:
        loop_check()
        data = self.request.body_arguments
        response_name = data['name'][0].decode('utf-8')  # bytes to str
        name = get_request_name(response_name)

        refresh = file_check.get_status(name)
        while not refresh:
            self.wait_future = file_check.cond.wait()
            try:
                await self.wait_future
            except asyncio.CancelledError:
                return
            refresh = file_check.get_status(name)
        file_check.refresh = False
        if self.request.connection.stream.closed():
            return
        refresh = 'true' if refresh else 'false'
        self.write(dict(should_refresh=refresh))

    def on_connection_close(self) -> None:
        self.wait_future.cancel()
