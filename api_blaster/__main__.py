import os
ROOT_DIR = os.path.abspath(os.curdir)

def main():
    try:
        from api_blaster.cli.cli import main
        exit_status = main()
    except KeyboardInterrupt:
        from httpie.status import ExitStatus
        exit_status = ExitStatus.ERROR_CTRL_C
    #
    # return exit_status.value


if __name__ == '__main__':  # pragma: nocover
    # import sys
    # sys.exit(main())
    main()