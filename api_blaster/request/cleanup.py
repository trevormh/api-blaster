import os
from pathlib import Path
from urllib.parse import urlsplit



def extract_response_body_and_meta(response_path: str, url: str):
    if not response_path or not os.path.isfile(response_path):
        print(f"invalid response file provided: {response_path}")
    url = get_base_url(url)
    new_response_path, new_filename = get_updated_path(response_path)  # new_response_path must be set
    tmp_file, header_end_line = create_tmp_response_file(response_path, url)
    update_response_file(response_path, tmp_file, header_end_line)
    # rename the response file with the correct extension
    rename_response_file(response_path, new_response_path)
    os.remove(tmp_file)  # delete tmp file
    return new_filename


def get_base_url(url: str):
    split = urlsplit(url)
    url = split.netloc
    if not split.scheme:
        return url
    return f'{split.scheme}://{url}/'


"""
The file was originally saved with a .txt extension.
Find the Content-Type from the response headers and return 
the path with the extension updated based on the content-type.
Ex: Content-Type = application/json
Return path with a json extension
"""
def get_updated_path(response_path: str) -> (str, str):
    extension = get_extension(response_path)
    p = Path(response_path)
    filename = f'{p.stem}{extension}'
    path = p.parts[:len(p.parts) - 1]
    return os.path.join(*path, filename), filename


"""
Requests are saved to a file by httpie with the headers
listed line by line, then a space, then the response body.

We need to find the content-type in the response headers to determine
what extension to save the response file 
"""
def get_extension(response_file: str) -> str:
    for line in read_file(response_file):
        if line.find('Content-Type') >= 0:
            if line.find('application/json') >= 0:
                return '.json'
            elif line.find('text/xml') >= 0:
                return '.xml'
            elif line.find('text/html') >= 0:
                return '.html'
        # elif line in ['\n', '\r\n']:
        #     # No content type was found.
        #     # An empty line either indicates we're on the space between header and body
        #     # or end of file has been reached.
        #     return '.txt'
    return '.txt'  # default to text if no matches are found


"""
This function is used to convert some relative url paths that 
might be in responses.

Also checks if headers are present in the file - this allows us
to check for the response content-type to know what extension the
"new" file should be saved with.
This also helps when writing the "new" file so we know ahead of time
that the first several lines are headers and should be skipped.
"""
def create_tmp_response_file(response_file: str, url: str) -> (str, int):
    file_split = response_file.rpartition('/')
    path = file_split[0]
    filename = file_split[2]
    tmp_filename = f"tmp_{filename}"  # create new file prefixed w/ "tmp"
    header_end_line = 0
    with open(tmp_file_path := os.path.join(path, tmp_filename), "w+") as tmp_file:
        for line_num, line in enumerate(read_file(response_file)):
            # There's a single empty line between headers and body
            # TODO - find better way to detect headers.
            if line in ['\n', '\r\n']:
                header_end_line = line_num
            line = line.replace('href="/', f'href="{url}')
            line = line.replace('src="/', f'src="{url}')
            line = line.replace("src='/", f'src="{url}')
            line = line.replace('content="/', f'content="{url}')
            line = line.replace('background:url(/', f'background:url({url}')
            tmp_file.write(line)
    return tmp_file_path, header_end_line



def update_response_file(response_path: str, tmp_response_path: str, header_end_line: int):
    with open(response_path, "w+", encoding="latin1") as response_path:
        for line_num, line in enumerate(read_file(tmp_response_path)):
            # Headers are saved to file initially because we need to get
            # the content-type of the response.
            # Headers are separated from the body by an empty line and
            # were detected by create_tmp_response_file function.
            # Don't write to the file until we iterate past this line num
            if line_num > header_end_line:
                response_path.write(line)


"""
Rename the response with the updated extension based on 
header content type
"""
def rename_response_file(old_path: str, new_path: str):
    os.rename(old_path, new_path)


def read_file(file: str):
    with open(file, 'r', encoding="latin1") as file:
        for line in file:
            yield line