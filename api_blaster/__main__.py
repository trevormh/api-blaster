import configparser
import os
from api_blaster.cfg import initialize_configs

from api_blaster.app_configs import AppConfigs

ROOT_DIR = os.path.abspath(os.curdir)


def main():
    # initialize_requests_dir()  # make sure it updates each time its imported
    global ROOT_DIR
    cfg = AppConfigs(ROOT_DIR)
    initialize_configs(ROOT_DIR)
    from api_blaster.cli.cli import main
    main()


if __name__ == '__main__':  # pragma: nocover
    main()
