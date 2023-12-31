import requests
from pathlib import Path
import logging
import json
import argparse

from download_functions import download_txt, download_image
from parse_functions import parse_book_page, get_books_url, get_latest_page
from requests_functions import get_response, check_for_redirect


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
    parser.add_argument(
        '-si',
        '--skip_images',
        action='store_true',
        help='Indicate this for not download images'
    )
    parser.add_argument(
        '-st',
        '--skip_texts',
        action='store_true',
        help='Indicate this for not download books',
    )
    parser.add_argument(
        '-d',
        '--dest_folder',
        type=str,
        help='Downloaded files saved on this path. Default: %(default)s',
        default=Path.cwd()
    )
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    start, end = args.start_page, args.end_page
    skip_images, skip_text = args.skip_images, args.skip_texts
    path = args.dest_folder
    path = Path(path)

    books_urls = []
    for page_number in range(start, end):
        url = f'https://tululu.org/l55/{page_number}/'
        try:
            urls = get_books_url(url)
            books_urls.extend(urls)
        except requests.HTTPError as err:
            logging.exception(err)
            logging.warning(f'страница с книгами "{url}" не найдена')
            continue
    parsed_books = []
    for url in books_urls:
        response = get_response(url)
        try:
            response.raise_for_status()
            check_for_redirect(response)
            parsed_book = parse_book_page(response.text, response.url)
            parsed_books.append(parsed_book)
        except requests.HTTPError as err:
            logging.exception(err)
            logging.warning(f'Страница книги "{url}" не найдена')
            continue
    json_file_path = path.joinpath('books.json')
    with open(json_file_path, 'w', encoding='UTF-8') as file:
        json.dump(parsed_books, file, ensure_ascii=False)

    for book in parsed_books:
        try:
            if not skip_text:
                download_txt(book['book_id'], book['title'], 'books', path=path)
            if not skip_images:
                download_image(book['image_url'], book['image_name'], path=path)
        except requests.HTTPError:
            logging.warning(f'Книги "{book["title"]}" нет на сайте')


if __name__ == '__main__':
    main()