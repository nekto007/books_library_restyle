import argparse
import os
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from requests import ConnectionError, HTTPError


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
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, f'{sanitize_filename(filename)}.txt')
    url = 'https://tululu.org/txt.php'
    parameters = {'id': book_id}
    response = requests.get(url, params=parameters)
    response.raise_for_status()
    check_for_redirect(response)
    book = response.text
    with open(filepath, 'w') as file:
        file.write(book)
    return filepath


def download_book_cover(image_url, folder='images/'):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, os.path.basename(image_url))
    response = requests.get(image_url)
    response.raise_for_status()
    book = response.content
    with open(filepath, 'wb') as file:
        file.write(book)
    return filepath


def parse_book_page(book_soup):
    title, author = book_soup.select_one('h1').text.split('::')

    image_path = book_soup.select_one('div .bookimage img')['src']

    comments_tag = book_soup.select('.texts')
    comments = [comment.select_one('span.black').text for comment in comments_tag]

    genre_tag = book_soup.select('span.d_book a')
    genres = [genre_tag.text for genre_tag in genre_tag]

    return {'title': title.strip(),
            'author': author.strip(),
            'genre': genres,
            'book_cover_url': image_path,
            'comments': comments}


def main():
    retry = 0
    parser = argparse.ArgumentParser()
    parser.add_argument('start_id', nargs='?', help='Enter start book id', type=int)
    parser.add_argument('end_id', nargs='?', help='Enter end book id', type=int)
    args = parser.parse_args()

    for book_id in range(args.start_id, args.end_id + 1):
        try:
            url = f'https://tululu.org/b{book_id}/'
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)
            book_soup = BeautifulSoup(response.text, 'lxml')
            book = parse_book_page(book_soup)
            download_book_cover(urljoin(url, book['book_cover_url']))
            download_txt(book_id, book.get('title'))
        except HTTPError:
            print(f'The book with id {book_id} could not be downloaded. Due to an error, skip it.')
        except ConnectionError:
            print('Connection error. Let\'s try again.')
            if retry:
                time.sleep(15)
            retry = 1


if __name__ == '__main__':
    main()
