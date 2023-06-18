import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit
import logging
import json
import argparse

from main import parse_book_page, download_txt, download_image, save_comments, check_for_redirect, get_response


def get_books_url(url):
    response = get_response(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    base = response.url
    selector = '#content table.d_book'
    books = soup.select(selector)
    books_urls = [urljoin(base, book.select_one('a')['href']) for book in books]
    return books_urls


def read_json_file(path='books.json'):
    with open(path, 'r', encoding='UTF-8') as file:
        json_file = file.read()
    parsed_books = json.loads(json_file)
    return parsed_books


def get_latest_page(url='https://tululu.org/l55/'):
    response = get_response(url)
    soup = BeautifulSoup(response.text, 'lxml')
    selector = '#content p.center a'
    latest = soup.select(selector)[-1].text
    return int(latest)


def create_parser():
    parser = argparse.ArgumentParser(description='Download books from tululu.org.')
    parser.add_argument(
        '-s',
        '--start_page',
        default=1,
        type=int,
        help='Start download from this id, default: %(default)s'
    )
    parser.add_argument(
        '-e',
        '--end_page',
        default=get_latest_page(),
        type=int,
        help='Complete download on this id, default: %(default)s'
    )
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    start, end = args.start_page, args.end_page
    books_urls = []
    for page in range(start, end):
        url = f'https://tululu.org/l55/{page}/'
        try:
            urls = get_books_url(url)
            books_urls.extend(urls)
        except requests.HTTPError:
            continue
    parsed_books = []
    for url in books_urls:
        response = get_response(url)
        response.raise_for_status()
        check_for_redirect(response)
        try:
            parsed_book = parse_book_page(response.text, response.url)
            parsed_books.append(parsed_book)
        except requests.HTTPError:
            continue
    #
    # with open('books.json', 'w', encoding='UTF-8') as file:
    #     json_books = json.dumps(parsed_books, ensure_ascii=False)
    #     file.write(json_books)

    # parsed_books = read_json_file()
    # pprint(parsed_books, sort_dicts=False)
    #
    for book in parsed_books:
        try:
            download_txt(book['book_id'], book['title'], 'books')
            download_image(book['image_url'], book['image_name'])
        except requests.HTTPError:
            logging.warning(f'Книги "{book["title"]}" нет на сайте')


if __name__ == '__main__':
    main()