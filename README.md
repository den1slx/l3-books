##  Парсер книг с сайта tululu.org
### Описание
Скачиваем книги, картинки и комментарии с [tululu](https://tululu.org/).

### Установка
- python3 должен быть установлен.
- Скачайте код.
- Установите зависимости командой:
```commandline
pip install -r requirements.txt
```

### Использование 
#### main
- Получите подсказку командой:
```commandline
python main.py -h
```
- Аргументы:
  * `-s` - Скачиваем книги начиная с этого id. Начальное значение учитывается.   
  * `-e` - Скачиваем книги заканчивая с этим id. Конечное значение не учитывается.  

- Пример:
```commandline
python main.py -s 10 -e 20
```
#### parse_tululu_category
- Получите подсказку командой:
```commandline
python main.py -h
```
- Аргументы:
  * `-s` - Скачиваем книги начиная с этой страницы. Начальное значение учитывается.   
  * `-e` - Скачиваем книги заканчивая с этой страницей. Конечное значение не учитывается.
  *  `-st` - Укажите чтобы не скачивать книги
  * `-si` - Укажите чтобы не скачивать картинки
  * `-d` - Путь по которому будут сохраняться файлы (папка images, папка books, и json-файл). Укажите существующий путь.
Пример пути: `'C:/Users/User/Новая папка'`

- Пример 1:
```commandline
parse_tululu_category.py -s 700
```
Будут скачаны книги с 700 и всех последующих страниц

- Пример 2:
```commandline
parse_tululu_category.py -s 625 -e 627 -si -st
```
Будет скачан только json-файл содержащий информацию о книгах со страниц 625 и 626

### Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).