import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import threading

os.system('cls')
def wrong(name):
    table =pd.read_excel(f'./{name}/{name}.xlsx')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0'}

    wrong_instrument = {'ticker': [],
                        'exchange': []}

    success_instrument = {'ticker': [],
                          'exchange': []}

    for i in range(len(table)):

        ticker = table['ticker']
        exchange = table['exchange']
        error = f'https://ru.tradingview.com/symbols/{exchange[i]}-{ticker[i]}/'

        full_page = requests.get(error, headers=headers)
        soup_error = BeautifulSoup(full_page.content, 'html.parser')

        try:
            pr = soup_error.find_all('h1', {'class': 'tv-http-error-page__title'})
            pr[0].text

        except:
           success_instrument['ticker'].append(ticker[i])
           success_instrument['exchange'].append(exchange[i])

        else:
            wrong_instrument['ticker'].append(ticker[i])
            wrong_instrument['exchange'].append(exchange[i])

        os.system('cls')
        print(f'{ticker[i]} | {exchange[i]} | {i}')
        print(f'{round(i / len(table)*100, 2)} %')

        wrong_table = pd.DataFrame(wrong_instrument)
        success_table = pd.DataFrame(success_instrument)

        if i % 50 == 0 or i == len(table):
            wrong_table.to_excel(f'./{name}/wrong {name}.xlsx', index=False)
            success_table.to_excel(f'./{name}/success {name}.xlsx', index=False)

    print(f'{name} ALL')

nasdaq = threading.Thread(target=wrong, args=('nasdaq'.upper(), ))
nyse = threading.Thread(target=wrong, args=('nyse'.upper(), ))
hkex = threading.Thread(target=wrong, args=('hkex'.upper(), ))
moex = threading.Thread(target=wrong, args=('moex'.upper(), ))

hkex.start()
nasdaq.start()