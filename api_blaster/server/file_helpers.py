import os


def get_file(responses_dir, filename):
    if not file_exists(responses_dir, filename):
        return f'Response {filename} not found'
    try:
        with open(os.path.join(responses_dir, filename), encoding="latin1") as file:
            return file.read()
    except Exception as e:  # TODO - better error handling
        return e


def file_exists(responses_dir, filename):
    if os.path.isfile(os.path.join(responses_dir, filename)):
        return True
    return False
