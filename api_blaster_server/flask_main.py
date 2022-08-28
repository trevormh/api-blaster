import os
import click
import logging
from flask import Flask


def create_app(response_dir, test_config=None):
    # print(response_dir)
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    """
    Flask uses click for logging.
    Override the secho and echo methods to prevent any messages
    from showing up on the console.
    """
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    def secho(text, file=None, nl=None, err=None, color=None, **styles):
        pass

    def echo(text, file=None, nl=None, err=None, color=None, **styles):
        pass

    click.echo = echo
    click.secho = secho

    app.config.from_pyfile('config.py', silent=True)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # response_reader blueprint registration
    import api_blaster_server.response_reader_bp as response_bp
    response_bp.set_responses_dir(response_dir)
    app.register_blueprint(response_bp.bp)

    return app
