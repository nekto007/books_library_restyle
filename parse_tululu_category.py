import argparse
import json
import os
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from requests import ConnectionError, HTTPError

from main import check_for_redirect, download_book_cover, download_txt, parse_book_page


def main():
    parser = argparse.ArgumentParser(
        description='Program download books from free online-library tululu.org'
    )
    parser.add_argument('--start_page', type=int, help='number of the first processed page', default=1)
    parser.add_argument('--end_page', type=int, help='number of the last processed page', default=2)
    parser.add_argument('--dest_folder', type=str,
                        help='path to the directory with parsing results: pictures, books, JSON.'
                        , default=os.getcwd())
    parser.add_argument('--skip_imgs', action='store_true', help='don\'t download pictures')
    parser.add_argument('--skip_txt', action='store_true', help='don\'t download book')
    parser.add_argument('--json_path', type=str, help='specify your path to the *.json file with the results'
                        , default='books')
    args = parser.parse_args()
    retry = 0
    all_books_links = []
    for page in range(args.start_page, args.end_page):
        try:
            url = f'https://tululu.org/l55/{page}'
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)
            category_soap = BeautifulSoup(response.text, 'lxml')
            books_tag = category_soap.select(' .d_book .bookimage a')
            book_links = [urljoin(url, books_tag.get('href')) for books_tag in books_tag]
            all_books_links += book_links
        except HTTPError:
            print(f'Error while handling page number {page}. Due to an error, skip it.')
        except ConnectionError:
            print('Connection error. Let\'s try again.')
            if retry:
                time.sleep(15)
            retry = 1
    books = []
    for book_url in all_books_links:
        os.chdir(os.path.normpath(args.dest_folder))
        try:
            response = requests.get(book_url)
            response.raise_for_status()
            check_for_redirect(response)
            book_soup = BeautifulSoup(response.text, 'lxml')
            book = parse_book_page(book_soup)
            if not args.skip_imgs:
                download_book_cover(urljoin(book_url, book['book_cover_url']))
            books.append(book)
            book_id = int(book_url[book_url.rfind('b') + 1:-1])
            if not args.skip_txt:
                download_txt(book_id, book.get('title'))
        except HTTPError:
            print(f'The book with id {book_id} could not be downloaded. Due to an error, skip it.')
        except ConnectionError:
            print('Connection error. Let\'s try again.')
            if retry:
                time.sleep(15)
            retry = 1
    with open(f'{args.json_path}.json', 'w') as file:
        json.dump(books, file, ensure_ascii=False)


if __name__ == '__main__':
    main()
