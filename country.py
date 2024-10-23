import multiprocessing

import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from functools import lru_cache
import threading
import time

os.system('cls')




@lru_cache
def find_country(exchange, number):
    table = pd.read_excel(f'./{exchange}/{exchange} data.xlsx', dtype=str)
    world = pd.read_excel(f'./table/country info.xlsx', dtype=str)
    world_country = []

    country_result = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0'}

    for j in world['country']:
        if j not in world_country:
            world_country.append(j)

    # base = {}
    #
    # for key in table:
    #     base[key] = []

    try:
        first = pd.read_excel(f'./{exchange}/{exchange} full data base.xlsx')

    except:
        begin = 0
    else:
        for cr in first['country']:
            country_result.append(cr)
        begin = len(first)

    for i in range(begin, len(table)):

        exchange = table['exchange'][i]
        ticker = table['ticker'][i]

        if exchange == 'HKEX':
            url = f'https://finance.yahoo.com/quote/{str(ticker).zfill(4)}.HK/profile'
        else:
            url = f'https://finance.yahoo.com/quote/{ticker}/profile'

        try:
            full_page = requests.get(url, headers=headers)
        except:
            continue

        soup = BeautifulSoup(full_page.content, 'html.parser')
        country = soup.find_all('div')

        os.system('cls')

        if len(country) < 161:
            print(f'{ticker}| {i}/{len(table)}')
            print(f'{ticker} | {exchange} | - | {url}')
            country_result.append('-')

        else:
            if country[161].text in world_country:
                print(f'{ticker}| {i}/{len(table)}')
                print(f'{ticker} | {exchange} | {country[number].text} | {url}')
                country_result.append(country[161].text)

            else:
                print(f'{ticker}| {i + 1}/{len(table)}')
                print(f'{ticker} | {exchange} | {country[number-1].text} | {url}')
                country_result.append(country[160].text)

        if i % 10 == 0 or i == len(table):

            base = {}
            for keys in table:
                base[keys] = []
                for value in table[keys].head(len(country_result)):
                    base[keys].append(value)
            base['country'] = country_result
            df = pd.DataFrame(base)
            df.to_excel(f'./{exchange}/{exchange} full data base.xlsx', index=False)
            time.sleep(5)

# tr1 = threading.Thread(target=find_country, args=('HKEX', 161))
# tr2 = threading.Thread(target=find_country, args=('NASDAQ', 161))
# tr3 = threading.Thread(target=find_country, args=('NYSE', 163))
# tr1.start()
# tr2.start()
# tr3.start()