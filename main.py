import requests
from pathlib import Path


path = Path.cwd().joinpath('books')
# path = Path(path_string)
Path.mkdir(path, parents=True, exist_ok=True)


for book_id in range(10):
    book_id += 1
    url = f"https://tululu.org/txt.php?id={book_id}"
    response = requests.get(url)
    response.raise_for_status()
    filename = f'book{book_id}.txt'
    with open(f'books/{filename}', 'wb') as file:
        file.write(response.content)
