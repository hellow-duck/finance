import pymysql
from config import *
import pandas as pd
import os
import uuid

os.system('cls')
# base = {'name': ['Anna', 'Oleg', 'Anastasia', 'Ekaterina', 'Dmitry', 'Maxim'],
#         'password': ['123456', 'qwerty', '654321', 'ytrewq', '1q2w3e', 'e3w2q1'],
#         'email': ['anna@gmail.com', 'oleg@gmail.com', 'nastya@gmail.com', 'katya@gmail.com', 'dmitry@gmail.com', 'maxim@gmail.com']}
base = pd.read_excel('./HKEX/HKEX information.xlsx')


try:
    connection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name
    )

    try:

        with connection.cursor() as cursor:
            create_table_query = ("CREATE TABLE IF NOT EXISTS `statement` (id INT AUTO_INCREMENT PRIMARY KEY, "
                                  "uuid VARCHAR(255) UNIQUE, "
                                  "name VARCHAR(255), "
                                  "ticker VARCHAR(255), "
                                  "exchange VARCHAR(255),"
                                  "sector VARCHAR(255),"
                                  "industry VARCHAR(255),"
                                  "CEO VARCHAR(255),"
                                  "main_office VARCHAR(255),"
                                  "page VARCHAR(255))")

            cursor.execute(create_table_query)
            print('Table created successfully!')

        with connection.cursor() as cursor:

            for value in range(len(base)):
                uuid_value = str(uuid.uuid4())  # Генерируем новый UUID
                insert_query = "INSERT INTO `statement` (uuid, name, ticker, exchange, sector, industry, CEO, main_office, page) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(insert_query, (uuid_value, base['name'][value], base['ticker'][value], base['exchange'][value], base['sector'][value], base['industry'][value], base['CEO'][value], base['main office'][value], base['page'][value]))

            connection.commit()
            print('information created successfully!')

    finally:
        connection.close()

except Exception as ex:
    print(ex)

