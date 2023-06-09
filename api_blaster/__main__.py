import os
import sys


def is_port_available(port_number: int) -> bool:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port_number)) != 0


def main():
    from api_blaster.settings.cfg import initialize_configs, get_config
    from api_blaster.settings.config_file_map import ConfigName

    ROOT_DIR = os.path.abspath(os.curdir)
    initialize_configs(ROOT_DIR)

    # check if flask server should be started
    if get_config(ConfigName.SERVER_STARTUP.value):
        response_dir = get_config(ConfigName.RESPONSES_DIR.value)
        port_number = int(get_config(ConfigName.PORT_NUMBER.value))
        if is_port_available(port_number):
            from .server.main import server_setup
            server_setup(response_dir, port_number)
        else:
            print(f'Server not started, port {port_number} is already in use. Change port number in settings to use server.')

    import api_blaster.cli.cli as cli
    sys.exit(cli.main())


if __name__ == '__main__':  # pragma: nocover
    sys.exit(main())
