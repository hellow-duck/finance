import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

os.system('cls')

ticker_mass = []
def info():
    url = 'https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities?sc_lang=en'
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)

    i = 1
    while True:
        try:
            button = driver.find_element(By.CSS_SELECTOR, '.loadmore')
            time.sleep(2)
            print(f'{i} | find')
            button.click()
        except:
            print('not find')
            break

        i += 1
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    result = soup.find_all('td', {'class' : 'code'})
    driver.quit()
    return result

information = info()
for i in information:
    ticker_mass.append(i.text)

df = pd.DataFrame({'ticker': ticker_mass})
df.to_excel('./HKEX.xlsx', index=False)



