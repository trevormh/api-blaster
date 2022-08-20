import os
from urllib.parse import urlsplit


def cleanup_response(response_file: str,  url: str):
    if not response_file or not os.path.isfile(response_file):
        print(f"invalid response file provided: {response_file}")
    url = get_base_url(url)
    tmp_file = create_tmp_response_file(response_file, url)
    update_response_file(response_file, tmp_file)
    os.remove(tmp_file)


def get_base_url(url: str):
    split = urlsplit(url)
    url = split.netloc
    if not split.scheme:
        return url
    return f'{split.scheme}://{url}/'


def create_tmp_response_file(response_file: str, url: str) -> str:
    file_split = response_file.rpartition('/')
    path = file_split[0]
    filename = file_split[2]
    tmp_filename = f"tmp_{filename}"  # create new file prefixed w/ "tmp"
    with open(tmp_file_path := os.path.join(path, tmp_filename), "w+") as tmp_file:
        for line in read_file(response_file):
            line = line.replace('href="/', f'href="{url}')
            line = line.replace('src="/', f'src="{url}')
            line = line.replace("src='/", f'src="{url}')
            line = line.replace('content="/', f'content="{url}')
            line = line.replace('background:url(/', f'background:url({url}')
            tmp_file.write(line)
    return tmp_file_path


def update_response_file(response_file, tmp_response_file):
    with open(response_file, "w+", encoding="latin1") as response_file:
        for line in read_file(tmp_response_file):
            response_file.write(line)


def read_file(file: str):
    with open(file, 'r', encoding="latin1") as file:
        for line in file:
            yield line