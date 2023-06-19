from pathlib import Path
from pathvalidate import sanitize_filename
from requests_functions import check_for_redirect, get_response


def download_txt(book_id, filename, folder, path=Path.cwd()):
    params = {'id': book_id}
    url = f"https://tululu.org/txt.php"
    filename = sanitize_filename(filename)
    path = path.joinpath(folder)

    response = get_response(url, params=params)
    response.raise_for_status()
    check_for_redirect(response)

    Path.mkdir(path, parents=True, exist_ok=True)

    fullpath = path.joinpath(f'{filename}.txt')
    with open(fullpath, 'wb') as file:
        file.write(response.content)

    return fullpath


def download_image(url, filename, folder='images', path=Path.cwd()):
    path = path.joinpath(folder)
    Path.mkdir(path, parents=True, exist_ok=True)
    response = get_response(url)
    response.raise_for_status()
    file_path = path.joinpath(filename)
    with open(file_path, 'wb') as file:
        file.write(response.content)


def save_comments(comments, book_id, folder):
    with open(f'{folder}/{book_id} comments.txt', 'w') as file:
        file.write(comments)
