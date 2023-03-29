import os

import requests

directory = 'books'
if not os.path.exists(directory):
    os.makedirs(directory, exist_ok=True)

url = 'https://tululu.org/txt.php?id='
for id in range(1, 11):
    response = requests.get(f'{url}{id}')
    response.raise_for_status()
    filename = f'{id}.txt'
    with open(f'{directory}/{filename}', 'w') as file:
        file.write(response.text)
