import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from requests import HTTPError


def check_for_redirect(response):
    if response.history:
        raise HTTPError


def download_txt(book_id, filename, folder='books/'):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, sanitize_filename(filename))
    url = f'https://tululu.org/txt.php?id={book_id}'
    response = requests.get(url)
    response.raise_for_status()
    book = response.text
    filename = f'{filepath}.txt'
    with open(filename, 'w') as file:
        file.write(book)
    return filename


def download_book_cover(book_soup, folder='images/'):
    bookimage_url = urljoin('https://tululu.org', book_soup.find('div', class_='bookimage').find('img')['src'])
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, os.path.basename(bookimage_url))
    url = bookimage_url
    response = requests.get(url)
    response.raise_for_status()
    book = response.text
    with open(filepath, 'w') as file:
        file.write(book)
    return filepath


def download_comments(book_soup):
    comments = book_soup.select('div.texts span')
    if comments:
        comment_text = [comment.text for comment in comments]
        return comment_text


def parse_book_page(book_soup):
    title, author = book_soup.find('h1').text.split('::')
    image_path = download_book_cover(book_soup)
    comments = download_comments(book_soup)
    genres = parse_book_genres(book_soup)
    return {'title': title.strip(),
            'author': author,
            'genre': genres,
            'book_cover_url': image_path,
            'comments': comments}


def parse_book_genres(book_soup):
    genre_tag = book_soup.select('span.d_book a')
    genres = [genre_tag.text for genre_tag in genre_tag]
    return genres


def main():
    for book_id in range(1, 11):
        try:
            url = f'https://tululu.org/b{book_id}/'
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)
            book_soup = BeautifulSoup(response.text, 'lxml')
            book = parse_book_page(book_soup)
            download_txt(book_id, book.get('title'))
        except HTTPError:
            pass


if __name__ == '__main__':
    main()
