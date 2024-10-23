import pandas as pd
import os

os.system('cls')
def math(name):

    table = pd.read_excel(f'./{name}/{name} finance math.xlsx')

    base = {'revenue': [],
            'net profit': [],
            'number of shares': []}

    price = []
    miss = ['—', 'not info', '‪0.00‬']

    for key in base:
        for value in table[key]:
            print(value)
            if value in miss:
                base[key].append(value)

            else:
                if type(value[-1]) == int:
                    base[key].append(float(value.replace('−', '-')))

                elif value[-1] == 'k'.upper():
                    value = value[:-1]
                    base[key].append(float(value.replace('−', '-')) * 10**3)

                elif value[-1] == 'm'.upper():
                    value = value[:-1]
                    base[key].append(float(value.replace('−', '-')) * 10**6)

                elif value[-1] == 'b'.upper():
                    value = value[:-1]
                    base[key].append(float(value.replace('−', '-')) * 10**9)

                elif value[-1] == 't'.upper():
                    value = value[:-1]
                    base[key].append(float(value.replace('−', '-')) * 10 ** 12)



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
    df.to_excel(f'./{name}/{name} finance math 2.xlsx', index=False)

math('HKEX')
math('NASDAQ')
math('NYSE')