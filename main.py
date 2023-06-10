from pathlib import Path

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_txt(url, filename, folder):
    filename = sanitize_filename(filename)
    path = Path.cwd().joinpath(folder)

    # path = Path(path_string)
    Path.mkdir(path, parents=True, exist_ok=True)
    try:
        response = requests.get(url)
        response.raise_for_status()
        check_for_redirect(response)
    except requests.HTTPError:
        return

    with open(f'{folder}/{filename}.txt', 'wb') as file:
        file.write(response.content)

    return path.joinpath(filename)


for book_id in range(10):
    book_id += 1
    book_url = f"https://tululu.org/txt.php?id={book_id}"
    page_url = f'https://tululu.org/b{book_id}/'
    try:
        response = requests.get(page_url)
        response.raise_for_status()
        check_for_redirect(response)
    except requests.HTTPError:
        continue
    soup = BeautifulSoup(response.text, 'lxml')
    title, author = soup.title.text.replace(', читать онлайн, скачать книгу бесплатно', '').split(' - ')
    # image = soup.find('div', class_='bookimage').find('img')['src']
    title = f'{book_id}. {title}'
    # download_txt(book_url, title, f'books/{author}')
    print(download_txt(book_url, title, 'books'))
