from requests import HTTPError

import argparse
import logging

from download_functions import download_txt, download_image, check_for_redirect, save_comments, get_response
from parse_functions import parse_book_page


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
        except HTTPError as error:
            logging.exception(error)
            logging.warning(f'Страница {page_url} не существует.')
            continue
        parsed_content = parse_book_page(response.text, response.url)
        title = f"{book_id}. {parsed_content['title']}"
        try:
            download_txt(book_id, title, 'books')
            save_comments(str(parsed_content['comments']), book_id, 'books')
            download_image(parsed_content['image_url'], parsed_content['image_name'])
        except HTTPError as error:
            logging.exception(error)
            logging.warning(f'Книги "{parsed_content["title"]}"({page_url}) нет на сайте', )


if __name__ == '__main__':
    main()
