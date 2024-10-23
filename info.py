import threading
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from functools import lru_cache

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0'}

@lru_cache
def Information(name):

    base = {'name': [],
            'ticker': [],
            'exchange': [],
            'sector': [],
            'industry': [],
            'page': []}

    table = pd.read_excel(f'./{name}/success {name}.xlsx')

    ticker = table['ticker']
    exchange = table['exchange']

    try:
        first = pd.read_excel(f'./{name}/{name} information 3.xlsx')

    except:
        begin = 0

    else:
        if len(table) <= len(first):
            print(f'{name} full data base')
            return

        for i in first:
            for key in first[i]:
                base[i].append(key)

        begin = len(first)


    for i in range(begin, len(table)):

        url = f'https://ru.tradingview.com/symbols/{exchange[i]}-{ticker[i]}/'
        full_page = requests.get(url, headers=headers)

        soup = BeautifulSoup(full_page.content, 'html.parser')

        base['ticker'].append(ticker[i])
        base['exchange'].append(exchange[i])

        os.system('cls')

        try:
            base['name'].append(soup.find_all('h1')[0].text)

        except:
            base['name'].append('-')

        try:
            base['sector'].append(soup.find_all('div', {'class': 'apply-overflow-tooltip'})[17].text)
        except:
            base['sector'].append('-')

        try:
            base['industry'].append(soup.find_all('div', {'class': 'apply-overflow-tooltip'})[19].text)
        except:
            base['industry'].append('-')

        try:
            base['page'].append(soup.find_all('a', {'class': 'link-GgmpMpKr'})[-1].get('href'))
        except:
            base['page'].append('-')

        print('-' * 40)
        for key in base:
            print(base[key][-1], ' | ', len(base[key]))
        print('-' * 40)

        if i % 50 == 0 or i == len(table) - 1:
            df = pd.DataFrame(base)
            df.to_excel(f'./{name}/{name} information 3.xlsx', index=False)


nasdaq = threading.Thread(target=Information, args=('nasdaq'.upper(), ))
nyse = threading.Thread(target=Information, args=('nyse'.upper(), ))
hkex = threading.Thread(target=Information, args=('hkex'.upper(), ))
moex = threading.Thread(target=Information, args=('moex'.upper(), ))

nasdaq.start()
nyse.start()
hkex.start()
moex.start()
