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
    url = f'https://www.moex.com/ru/marketdata/#/mode=groups&group=4&collection=3&boardgroup=57&data_type=current&category=main'

    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    page_num = soup.find_all('button', {'class': 'UiPaginationButton_buttonNew_KSmaR'})
    i = 1
    while True:
        if i > int(page_num[-2].text):
            break
        os.system('cls')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tickers = soup.find_all('div', {'class': 'SecValue_cell_1T6mS'})
        for j in range(len(tickers)):
            print(tickers[j].text)
            ticker_mass.append(tickers[j].text)

        button = driver.find_element(By.CSS_SELECTOR, 'button.UiPaginationButton_buttonNew_KSmaR:nth-child(9)')
        print(f'{i} | find | {len(ticker_mass)}')

        try:
            button.click()
            time.sleep(2)

        except:
            print(f'not find')
            break

        i += 1
    driver.close()

    df = pd.DataFrame({'ticker': ticker_mass})
    df.to_excel('./MOEX.xlsx')

info()