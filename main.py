from pathlib import Path

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin
import argparse
import logging
from time import sleep


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_txt(book_id, filename, folder):
    params = {'id': book_id}
    url = f"https://tululu.org/txt.php"
    filename = sanitize_filename(filename)
    path = Path.cwd().joinpath(folder)

    response = get_response(url, params=params)
    response.raise_for_status()
    check_for_redirect(response)

    Path.mkdir(path, parents=True, exist_ok=True)

    fullpath = path.joinpath(f'{filename}.txt')
    with open(fullpath, 'wb') as file:
        file.write(response.content)

    return fullpath


def download_image(url, filename, folder='images'):
    path = Path.cwd().joinpath(folder)
    Path.mkdir(path, parents=True, exist_ok=True)
    response = get_response(url)
    response.raise_for_status()
    with open(f'{folder}/{filename}', 'wb') as file:
        file.write(response.content)


def save_comments(comments, book_id, folder):
    with open(f'{folder}/{book_id} comments.txt', 'w') as file:
        file.write(comments)


def get_genres(soup):
    genres = soup.find('span', class_='d_book').find_all('a')
    genres = [genre.text for genre in genres]
    return genres


def get_comments(soup):
    soup_comments = soup.body.table.find_all('div', class_='texts')
    comments = ''
    for comment in soup_comments:
        comments += f'{comment.span.text}\n'
    return comments


def get_image_url(soup, base_url):
    image_address = soup.find('div', class_='bookimage').find('img')['src']
    image_url = urljoin(base_url, image_address)
    return image_url


def parse_book_page(html_page, base_url):
    soup = BeautifulSoup(html_page, 'lxml')
    splited_text = soup.title.text.replace(', читать онлайн, скачать книгу бесплатно', '').split(' - ')
    if len(splited_text) > 2:
        author = splited_text[-1]
        splited_text.pop()
        title = ' - '.join(splited_text)
    else:
        title, author = splited_text

    image_url = get_image_url(soup, base_url)
    image_name = image_url.split('/')[-1]
    parsed_content = {
        'author': author,
        'title': title,
        'genres': get_genres(soup),
        'comments': get_comments(soup),
        'image_url': image_url,
        'image_name': image_name,
    }
    return parsed_content


def get_response(url, params=None, await_time=10):
    while True:
        try:
            response = requests.get(url, params)
            break
        except requests.ConnectionError as err:
            logging.exception(err)
            logging.error('Проверьте интернет соединение, ожидание подключения.')
            sleep(await_time)

    return response


def create_parser():
    parser = argparse.ArgumentParser(description='Download books from tululu.org.')
    parser.add_argument(
        '-s',
        '--start_id',
        default=1,
        type=int,
        help='Start download from this id, default: %(default)s'
    )
    parser.add_argument(
        '-e',
        '--end_id',
        default=10,
        type=int,
        help='Complete download on this id, default: %(default)s'
    )
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    start_id, end_id = args.start_id, args.end_id
    for book_id in range(start_id, end_id):
        page_url = f'https://tululu.org/b{book_id}/'
        try:
            response = get_response(page_url)
            response.raise_for_status()
            check_for_redirect(response)
        except requests.HTTPError as error:
            logging.exception(error)
            logging.warning(f'Страница {page_url} не существует.')
            continue
        parsed_content = parse_book_page(response.text, response.url)
        title = f"{book_id}. {parsed_content['title']}"
        try:
            download_txt(book_id, title, 'books')
            save_comments(parsed_content['comments'], book_id, 'books')
            download_image(parsed_content['image_url'], parsed_content['image_name'])
        except requests.HTTPError as error:
            logging.exception(error)
            logging.warning(f'Книги "{parsed_content["title"]}"({page_url}) нет на сайте', )


if __name__ == '__main__':
    main()
