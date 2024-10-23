import os
import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import pandas as pd

os.system('cls')

ticker_mass = []
chromedriver_autoinstaller.install()

def info():
    url = f'https://www.nasdaq.com/market-activity/stocks/screener '

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup.find_all()
    i = 1
    while True:
        os.system('cls')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tickers = soup.find_all('a', {'class': 'firstCell'})
        for j in range(len(tickers)):
            if j % 2 == 0:
                print(tickers[j].text)
                ticker_mass.append(tickers[j].text)
            else:
                pass

        try:
            
            button = driver.find_element(By.CSS_SELECTOR, '.pagination__next')
            print(f'{i} | find | {len(ticker_mass)}')
            button.click()
            time.sleep(2)

        except:
            print(f'not find')
            break

        i += 1
    driver.close()

    df = pd.DataFrame({'ticker': ticker_mass})
    df.to_excel('./NASDAQ.xlsx')

info()