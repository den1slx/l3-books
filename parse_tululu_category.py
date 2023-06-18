import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_response(url):
    response = requests.get(url)
    response.raise_for_status()
    return response


def get_books_url(url):
    response = get_response(url)
    soup = BeautifulSoup(response.text, 'lxml')
    base = response.url
    books = soup.find('div', id='content').find_all('table', class_='d_book')
    books_urls = [urljoin(base, book.find('a')['href']) for book in books]
    return books_urls


def main():
    books_urls = []
    for page in range(1, 11):
        url = f'https://tululu.org/l55/{page}/'
        books_urls.extend(get_books_url(url))

    print(len(books_urls))
    print(books_urls)


if __name__ == '__main__':
    main()

