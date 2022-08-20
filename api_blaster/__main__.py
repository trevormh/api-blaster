import os

def start_server(response_dir):
    if not os.path.isdir(response_dir):
        print(f'Flask server was not started. Invalid response directory provided: {response_dir}')
        return
    from api_blaster_server.main import create_app
    app = create_app(response_dir)
    app.run(host='0.0.0.0', port=8000)


if __name__ == '__main__':  # pragma: nocover
    import sys

    from api_blaster.settings.cfg import initialize_configs, get_config
    from api_blaster.settings.config_file_map import ConfigName, ConfigFileName

    ROOT_DIR = os.path.abspath(os.curdir)
    initialize_configs(ROOT_DIR)

    # check if flask server should be started
    if get_config(ConfigName.SERVER_STARTUP.value):
        import threading
        response_dir = get_config(ConfigName.RESPONSES_DIR.value)
        server_thread = threading.Thread(target=start_server, args=(response_dir,), daemon=True)
        server_thread.start()

    import api_blaster.cli.cli as cli
    sys.exit(cli.main())
