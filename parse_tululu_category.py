import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit
from pprint import pprint
import logging
import json

from main import parse_book_page, download_txt, download_image, save_comments, check_for_redirect, get_response


def get_books_url(url):
    response = get_response(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    base = response.url
    books = soup.find('div', id='content').find_all('table', class_='d_book')
    books_urls = [urljoin(base, book.find('a')['href']) for book in books]
    return books_urls


def read_json_file(path='books.json'):
    with open(path, 'r', encoding='UTF-8') as file:
        json_file = file.read()
    parsed_books = json.loads(json_file)
    return parsed_books


def main():
    # books_urls = []
    # start = 1  # for parser
    # end = 5  # for parser
    # for page in range(start, end):
    #     url = f'https://tululu.org/l55/{page}/'
    #     try:
    #         urls = get_books_url(url)
    #         books_urls.extend(urls)
    #     except requests.HTTPError:
    #         continue
    #
    # parsed_books = []
    # for url in books_urls:
    #     response = get_response(url)
    #     response.raise_for_status()
    #     check_for_redirect(response)
    #     try:
    #         parsed_book = parse_book_page(response.text, response.url)
    #         parsed_books.append(parsed_book)
    #     except requests.HTTPError:
    #         continue
    #
    # with open('books.json', 'w', encoding='UTF-8') as file:
    #     json_books = json.dumps(parsed_books, ensure_ascii=False)
    #     file.write(json_books)

    parsed_books = read_json_file()
    # pprint(parsed_books, sort_dicts=False)

    for book in parsed_books:
        try:
            download_txt(book['book_id'], book['title'], 'books')
            # save_comments(str(book['comments']), book['book_id'], 'books')
            # download_image(book['image_url'], book['image_name'])
        except requests.HTTPError as error:
            # logging.exception(error)
            logging.warning(f'Книги "{book["title"]}" нет на сайте')


if __name__ == '__main__':
    main()

