import os
import sys
ROOT_DIR = os.path.abspath(os.curdir)

if __name__ == '__main__':  # pragma: nocover
    from api_blaster.settings.cfg import initialize_configs
    initialize_configs(ROOT_DIR)
    from api_blaster.cli.cli import main
    sys.exit(main())
