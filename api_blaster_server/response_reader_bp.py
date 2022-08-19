from flask import (
    Blueprint, flash, g, redirect, render_template, render_template_string, request, session, url_for
)
import os


bp = Blueprint('response_reader', __name__, url_prefix='/')

responses_dir = ''


def set_responses_dir(resp_dir):
    global responses_dir
    responses_dir = resp_dir


@bp.route('/response/<response_name>')
def hello(response_name):
    # return get_file(response_name)
    return get_file(response_name)


def get_file(filename):
    with open(os.path.join(responses_dir, filename), encoding="latin1") as file:
        return file.read()
