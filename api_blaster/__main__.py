import os



ROOT_DIR = os.path.abspath(os.curdir)


def start_server():
    import logging
    from api_blaster_server.main import create_app
    app = create_app()
    log = logging.getLogger('werkzeug')
    log.disabled = True
    app.run(host='0.0.0.0', port=8000)  # change port according to your needs


if __name__ == '__main__':  # pragma: nocover
    import sys
    from api_blaster.settings.cfg import initialize_configs, get_config
    from api_blaster.settings.config_file_map import ConfigName

    initialize_configs(ROOT_DIR)

    startup_cfg_name = ConfigName('SERVER_STARTUP').value
    if get_config(startup_cfg_name):
        import threading
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()

    from api_blaster.cli.cli import main
    sys.exit(main())
