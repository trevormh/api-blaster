import asyncio
import tornado.escape
import tornado.locks
import tornado.web
import os.path

from tornado.options import define, options, parse_command_line

from api_blaster_server.request_handlers.content_handler import ContentHandler
from api_blaster_server.request_handlers.most_recent_handler import MostRecentHandler
from api_blaster_server.request_handlers.refresh_handler import RefreshHandler
from api_blaster_server.request_handlers.test_handler import TestHandler

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")


async def main(responses_dir: str):
    # TODO - better error handling
    if not responses_dir:
        print('Responses directory not set - Cannot start server')
        return

    import logging
    hn = logging.NullHandler()
    hn.setLevel(logging.DEBUG)
    logging.getLogger("tornado.access").addHandler(hn)
    logging.getLogger("tornado.access").propagate = False
    logging.getLogger('tornado.access').disabled = True

    # Parses all options given on the command line
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/test", TestHandler),
            (r"/refesh", RefreshHandler),
            (r"/most_recent/.*", MostRecentHandler, dict(responses_dir=responses_dir)),
            (r"/content/.*", ContentHandler, dict(responses_dir=responses_dir)),
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
