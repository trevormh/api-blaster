import asyncio
import threading
from typing import Union

import tornado.escape
import tornado.locks
import tornado.web
import os.path

from tornado.options import define, options, parse_command_line


from api_blaster.settings.cfg import get_config
from api_blaster.settings.config_file_map import ConfigName
from api_blaster.server.request_handlers.content_handler import ContentHandler
from api_blaster.server.request_handlers.most_recent_handler import MostRecentHandler
from api_blaster.server.request_handlers.refresh_handler import RefreshHandler
from api_blaster.server.request_handlers.test_handler import TestHandler

shutdown_event: Union[asyncio.Event, None] = None
server: Union['tornado.web.Application', None] = None


async def main(responses_dir: str, port_number: int):
    # TODO - better error handling
    if not responses_dir:
        print('Responses directory not set - Cannot start server')
        return
    elif not port_number:
        print('Port number not set - Cannot start server')
        return

    try:
        options.port = port_number
    except AttributeError:
        define("port", default=port_number, help="run on the given port", type=int)
        define("debug", default=False, help="run in debug mode")

    import logging
    hn = logging.NullHandler()
    hn.setLevel(logging.DEBUG)
    logging.getLogger("tornado.access").addHandler(hn)
    logging.getLogger("tornado.access").propagate = False
    logging.getLogger('tornado.access').disabled = True

    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/api-blaster-get-test", TestHandler),
            (r"/api-blaster-post-test", TestHandler),
            (r"/refesh", RefreshHandler),
            (r"/most_recent/.*", MostRecentHandler, dict(responses_dir=responses_dir)),
            (r"/content/.*", ContentHandler, dict(responses_dir=responses_dir)),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        idle_connection_timeout=5,
        debug=False,
        autoreload=False
    )
    global server
    server = app.listen(options.port)
    global shutdown_event
    shutdown_event = asyncio.Event()
    await shutdown_event.wait()


def start_server(responses_dir: str, port_number: int):
    print(f'Starting server on port {port_number}')
    asyncio.run(main(responses_dir, port_number))


server_thread: Union[threading.Thread, None] = None


def server_setup(responses_dir: str, port_number: int):
    try:
        global server_thread
        server_thread = threading.Thread(target=start_server, args=(responses_dir, port_number), daemon=True)
        server_thread.start()
    except Exception as e:
        print(e)


def stop_server():
    try:
        server.stop()
        shutdown_event.set()
        asyncio.run(server.close_all_connections())
    except asyncio.exceptions.CancelledError as e:
        pass
    except Exception as e:
        pass
    finally:
        server_thread.join(timeout=1)


def restart_server():
    stop_server()
    response_dir = get_config(ConfigName.RESPONSES_DIR.value)
    port_number = int(get_config(ConfigName.PORT_NUMBER.value))
    server_setup(response_dir, port_number)
