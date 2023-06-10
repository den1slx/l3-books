from pathlib import Path

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_txt(book_id, filename, folder):
    params = {'id': book_id}
    url = f"https://tululu.org/txt.php"
    filename = sanitize_filename(filename)
    path = Path.cwd().joinpath(folder)
    # path = Path(path_string)

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        check_for_redirect(response)
    except requests.HTTPError:
        return

    Path.mkdir(path, parents=True, exist_ok=True)
    with open(f'{folder}/{filename}.txt', 'wb') as file:
        file.write(response.content)

    return path.joinpath(filename)


def download_image(url, filename, folder='images'):
    path = Path.cwd().joinpath(folder)
    Path.mkdir(path, parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    with open(f'{folder}/{filename}', 'wb') as file:
        file.write(response.content)


for book_id in range(10):
    book_id += 1
    url = 'https://tululu.org'
    page_url = f'https://tululu.org/b{book_id}/'
    try:
        response = requests.get(page_url)
        response.raise_for_status()
        check_for_redirect(response)
    except requests.HTTPError:
        continue
    soup = BeautifulSoup(response.text, 'lxml')
    title, author = soup.title.text.replace(', читать онлайн, скачать книгу бесплатно', '').split(' - ')
    title = f'{book_id}. {title}'
    # save_path = download_txt(book_url, title, f'books/{author}')
    save_path = download_txt(book_id, title, 'books')
    if save_path:
        image = soup.find('div', class_='bookimage').find('img')['src']
        image_name = image.split('/')[-1]
        image_url = urljoin(url, image)
        download_image(image_url, image_name)
