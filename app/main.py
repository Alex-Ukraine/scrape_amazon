from pathlib import Path
import csv

from selenium import webdriver
from bs4 import BeautifulSoup

# .resolve() - makes the path absolute
DRIVER_PATH = str(Path('geckodriver').resolve())
BROWSER = webdriver.Firefox(executable_path=DRIVER_PATH)


def write_csv(ads):
    with open('results.csv', 'a') as f:
        fields = ['title', 'price', 'url']
        writer = csv.DictWriter(f, fieldnames=fields)

        for ad in ads:
            writer.writerow(ad)


def get_html(url):
    BROWSER.get(url)
    return BROWSER.page_source


def scrape_data(card):
    try:
        h2 = card.h2
    except:
        title = ''
        url = ''
    else:
        title = h2.text.strip()
        url = h2.a.get('href')

    try:
        price = card.find('span', class_='a-price-whole').text.strip('.').strip()
    except:
        price = ''
    else:
        price = ''.join(price.split(','))

    data = {'title': title, 'url': url, 'price': price}

    return data


def main():
    ads_data = []
    for i in range(1, 4):
        url = f'https://www.amazon.com/s?k=canon+5d&page={i}&qid=1627491582&ref=sr_pg_2'
        html = get_html(url)

        soup = BeautifulSoup(html, 'lxml')

        cards = soup.find_all('div', {'data-asin': True,
                                      'data-component-type': 's-search-result'})

        for card in cards:
            data = scrape_data(card)
            ads_data.append(data)

    write_csv(ads_data)


if __name__ == '__main__':
    main()
