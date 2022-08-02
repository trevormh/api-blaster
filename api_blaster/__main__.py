import os
from api_blaster.settings.cfg import initialize_configs

ROOT_DIR = os.path.abspath(os.curdir)


def main():
    initialize_configs(ROOT_DIR)
    from api_blaster.cli.cli import main
    main()


if __name__ == '__main__':  # pragma: nocover
    main()
