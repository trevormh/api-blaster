from flask import (
    Blueprint, flash, g, redirect, render_template, render_template_string, request, session, url_for
)
import os

bp = Blueprint('response_reader', __name__, url_prefix='/')

responses_dir = ''


# This function is called when setting up the Flask app in the create_app function
def set_responses_dir(resp_dir):
    global responses_dir
    responses_dir = resp_dir


# Returns the most recent response for a given request name
# Ex: 5 responses exist for the "google-get" request, the most recent will be returned
@bp.route('/most_recent/<filename>')
def response_by_name(filename):
    file_split = filename.split("request=")
    if len(file_split) == 2:
        request_name = file_split[1]
        return get_most_recent(request_name)
    else:
        return f'Response {filename} not found'


def get_most_recent(request_name):
    from pathlib import Path
    pattern = rf'*request={request_name}'
    path_dir = Path(responses_dir)
    try:
        latest = max(path_dir.glob(pattern), key=os.path.getctime)
        return get_file(latest)
    except ValueError:
        return f'No requests found for {request_name}'


# Return a response by filename from the responses directory
@bp.route('/response_by_filename/<filename>')
def response_by_filename(filename):
    return get_file(filename)


def get_file(filename):
    if not file_exists(filename):
        return f'Response {filename} not found'
    try:
        with open(os.path.join(responses_dir, filename), encoding="latin1") as file:
            return file.read()
    except Exception as e:  # TODO - better error handling
        return e


def file_exists(filename):
    if os.path.isfile(os.path.join(responses_dir, filename)):
        return True
    return False
