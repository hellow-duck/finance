import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import re
import chromedriver_autoinstaller
import multiprocessing
import functools

os.system('cls')

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('log-level=3')

driver = webdriver.Chrome(options=options)


@functools.lru_cache(maxsize=100)
def finance(key):
    table = pd.read_excel(f'./{key}/{key} information.xlsx', dtype=str)

    base = {'revenue': [],
            'net profit': [],
            'number of shares': [],
            'price': []}

    # Чтение сохраненного файла
    try:
        first = pd.read_excel(f'./{key}/{key} finance.xlsx')

    except:
        print(f'{key} finance not found...')
        time.sleep(5)
        begin = 0
    else:
        print(f'{key} finance found...')
        time.sleep(5)
        for i in base:
            for j in first[i]:
                base[i].append(j)

        begin = len(first)

    # Цикл создания нового файла/изменение уже сусществующего
    for number in range(begin, len(table)):

        tickers = table['ticker'][number]
        exchanges = table['exchange'][number]

        url = f'https://en.tradingview.com/symbols/{exchanges}-{tickers}/financials-income-statement/?statements-period=FY'
        td = {}


        driver.get(url)

        # input('press key...')
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        try:
            soup.find_all('h1', {'class': 'tv-http-error-page__title'})[0].text
        except:
            None
        else:
            pass

        strait = soup.find_all('span', {'class': 'titleText-C9MdAMrq withLink-C9MdAMrq'})
        profit = soup.find_all('div', {'class': 'values-C9MdAMrq values-AtxjAQkN'})

        for str_head in strait:
            td[str_head.text] = []

        a = [0]
        for str_body in td:
            b = a[-1]
            for body in profit[b]:
                body = body.text.replace('‪‪', '').replace('‬‬−', '+').replace('\u202f', '').replace('‬‬', '')

                body = re.sub(r'\+.*$', '', body)
                td[str_body].append(body)

                a.append(b + 1)

        try:
            base['revenue'].append(td['Total revenue'][6])
        except:
            base['revenue'].append('not info')

        try:
            base['net profit'].append(td['Net income'][6])
        except:
            base['net profit'].append('not info')

        try:
            base['number of shares'].append(td['Diluted shares outstanding'][6])
        except:
            base['number of shares'].append('not info')

        try:
            base['price'].append(soup.find_all('span', {'class': 'last-JWoJqCpY js-symbol-last'})[-1].text)
        except:
            base['price'].append('not info')

        os.system('cls')
        print('-' * 60)
        print(f'{tickers} | {exchanges}')
        print(f'{number + 1} / {len(table)}')
        print('-' * 60)


        if (number % 50 == 0 and number != 0) or number + 1 == len(table):
            data = {'name': table['name'].head(len(base['revenue'])),
                    'ticker': table['ticker'].head(len(base['revenue'])),
                    'exchange': table['exchange'].head(len(base['revenue'])),
                    'sector': table['sector'].head(len(base['revenue'])),
                    'industry': table['industry'].head(len(base['revenue'])),
                    'page': table['page'].head(len(base['revenue'])),
                    'revenue': base['revenue'],
                    'net profit': base['net profit'],
                    'number of shares': base['number of shares'],
                    'price': base['price']}

            tablet = pd.DataFrame(data)
            tablet.to_excel(f'./{key}/{key.upper()} finance.xlsx', index=False)

    driver.close()
    driver.quit()

# Перевод в целые числа
def math(name):

    table = pd.read_excel(f'./{name}/{name} finance.xlsx')

    base = {'revenue': [],
            'net profit': [],
            'number of shares': []}

    price = []
    miss = ['—', 'not info', '‪0.00‬']

    for key in base:
        for value in table[key]:
            if value in miss:
                base[key].append(value)

            else:
                if value[-1] == 'k'.upper():
                    value = value[:-1]
                    base[key].append(float(value.replace('−', '-')) * 10**3)

                elif value[-1] == 'm'.upper():
                    value = value[:-1]
                    base[key].append(float(value.replace('−', '-')) * 10**6)

                elif value[-1] == 'b'.upper():
                    value = value[:-1]
                    base[key].append(float(value.replace('−', '-')) * 10**9)

                elif type(value[-1]) == int:
                    base[key].append(float(value.replace('−', '-')))

                else:
                    base[key].append(value.replace('.', ','))
        print(f'{name} | {key} | {len(base[key])}')

    for stock in table['price']:
        price.append(str(stock).replace('.', ','))

    print(f'{name} | price | {len(price)} \n')

    data = {'name': table['name'],
            'ticker': table['ticker'],
            'exchange': table['exchange'],
            'sector': table['sector'],
            'industry': table['industry'],
            'page': table['page'],
            'revenue': base['revenue'],
            'net profit': base['net profit'],
            'number of shares': base['number of shares'],
            'price': price}

    df = pd.DataFrame(data)
    df.to_excel(f'./{name}/{name} finance.xlsx', index=False)

if __name__ == '__main__':
    multiprocessing.freeze_support()

    processes = []

    # finance('HKEX')
    processes.append(multiprocessing.Process(target=finance, args=('HKEX',)))
    processes.append(multiprocessing.Process(target=finance, args=('NASDAQ',)))
    processes.append(multiprocessing.Process(target=finance, args=('NYSE',)))

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    math('HKEX')
    math('NYSE')
    math('NASDAQ')