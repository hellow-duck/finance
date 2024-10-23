import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import chromedriver_autoinstaller
import asyncio

os.system('cls')
chromedriver_autoinstaller.install()
table = pd.read_excel(f'./success HKEX.xlsx')
tickers = []

for i in table['ticker'].head(20):
    tickers.append(i)

async def finance(ticker):
    
    url = f'https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities/Equities-Quote?sym={ticker}&sc_lang=en'

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('log-level=3')
    

    driver = webdriver.Chrome(options=options)

    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    name = soup.find_all('span', {'class' : 'col_longname'})
    price = soup.find_all('span', {'class' : 'col_last'})
    symbols = soup.find_all('dt', {'class' : 'ico_data'})

    print(f'{name[-1].text.replace(f'({ticker})', '')} | {price[-1].text} | {symbols[3].text} | {symbols[9].text.replace('x', '')}')

async def process(ticker):
    tasks = [finance(ticker=ticker) for url in ticker]
    await asyncio.gather(*tasks)

asyncio.run(process(tickers))