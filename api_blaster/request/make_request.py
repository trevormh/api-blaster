from imp import reload

from api_blaster.event import event

import httpie.core


def make_request(cmd: list):
    httpie.core.main(cmd)


@event.on("reload_httpie")
def reload_httpie():
    """
    When the suppress output setting is toggled from True
    to False, httpie will not reflect the setting change
    until it is reloaded
    """
    reload(httpie.core)
