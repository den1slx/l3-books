from pathlib import Path

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin
import argparse


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


def download_comments(comments, book_id, folder):
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


def get_image(soup, base_url):
    image_address = soup.find('div', class_='bookimage').find('img')['src']
    image_name = image_address.split('/')[-1]
    image_url = urljoin(base_url, image_address)
    return image_url, image_name


def parse_book_page(html_page, base_url):
    soup = BeautifulSoup(html_page, 'lxml')
    splited_text = soup.title.text.replace(', читать онлайн, скачать книгу бесплатно', '').split(' - ')
    if len(splited_text) > 2:
        author = splited_text[-1]
        splited_text.pop()
        title = ' - '.join(splited_text)
    else:
        title, author = splited_text

    image_url, image_name = get_image(soup, base_url)
    parsed_content = {
        'author': author,
        'title': title,
        'genres': get_genres(soup),
        'comments': get_comments(soup),
        'image_url': image_url,
        'image_name': image_name,
    }
    return parsed_content


def create_parser():
    parser = argparse.ArgumentParser(description='download books from tululu.org')
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
            response = requests.get(page_url)
            response.raise_for_status()
            check_for_redirect(response)
        except requests.HTTPError:
            continue
        parsed_content = parse_book_page(response.text, response.url)
        title = f"{book_id}. {parsed_content['title']}"
        save_path = download_txt(book_id, title, 'books')
        if save_path:
            download_comments(parsed_content['comments'], book_id, 'books')
            download_image(parsed_content['image_url'], parsed_content['image_name'])


if __name__ == '__main__':
    main()