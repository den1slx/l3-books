from pathlib import Path

import requests


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


path = Path.cwd().joinpath('books')
# path = Path(path_string)
Path.mkdir(path, parents=True, exist_ok=True)


for book_id in range(10):
    book_id += 1
    url = f"https://tululu.org/txt.php?id={book_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        check_for_redirect(response)
    except requests.HTTPError:
        continue

    filename = f'book{book_id}.txt'
    with open(f'books/{filename}', 'wb') as file:
        file.write(response.content)
