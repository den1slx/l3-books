from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit
from requests_functions import get_response, check_for_redirect


def get_genres(soup):
    selector = 'span.d_book a'
    genres = soup.select(selector)
    genres = [genre.text for genre in genres]
    return genres


def get_comments(soup):
    selector = 'table div.texts '
    soup_comments = soup.select(selector)
    comments = [comment.span.text for comment in soup_comments]
    return comments


def get_image_url(soup, base_url):
    selector = 'div.bookimage img'
    image_address = soup.select_one(selector)['src']
    image_url = urljoin(base_url, image_address)
    return image_url


def get_book_id(url):
    book_id = urlsplit(url).path.lstrip('/b').rstrip('/')
    return book_id


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
        'book_id': get_book_id(base_url),
    }
    return parsed_content


def get_books_url(url):
    response = get_response(url)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'lxml')
    base = response.url
    selector = '#content table.d_book'
    books = soup.select(selector)
    books_urls = [urljoin(base, book.select_one('a')['href']) for book in books]
    return books_urls


def get_latest_page(url='https://tululu.org/l55/'):
    response = get_response(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    selector = '#content p.center a'
    latest = soup.select(selector)[-1].text
    return int(latest) + 1