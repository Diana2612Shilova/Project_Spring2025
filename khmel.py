import requests
import pandas as pd
import re
import numpy as np
from bs4 import BeautifulSoup
response = requests.get('https://malt.ru/catalog/khmel/')
soup = BeautifulSoup(response.text, 'html.parser')
data =[]
cards = soup.find_all("div", class_="productCardDescription")
for card in cards:
    title_tag = card.find("a")
    title = title_tag.get_text(strip=True)

    kislotnost_tag = card.find("div", class_="productCardColor")
    kislotnost = kislotnost_tag.get_text(strip=True).replace(" ", "")

    price_tag = card.find("p", class_="priceText newPrice")
    if price_tag:
        price = price_tag.get('data-price-per-kg').split("<")[0]
        price = price.replace(" ", '')
    else:
        price = None

    data.append({
            "Название": title,
        'Кислотность': kislotnost,
        'Цена за килограмм': price
        })

df = pd.DataFrame(data)
for i, row in enumerate(df['Кислотность']):
    if '-' in row:
        df.loc[i, 'Кислотность минимальная'] = row.split('-')[0]
        df.loc[i,'Кислотность максимальная'] = row.split('-')[1]
        df.loc[i, 'Кислотность минимальная'] = df.loc[i,'Кислотность минимальная'].replace('%', '')
        df.loc[i, 'Кислотность максимальная'] = df.loc[i, 'Кислотность максимальная'].replace('%', '')
        df.loc[i, 'Кислотность минимальная'] = df.loc[i, 'Кислотность минимальная'].replace(',', '.')
        df.loc[i, 'Кислотность максимальная'] = df.loc[i, 'Кислотность максимальная'].replace(',', '.')
        df.loc[i, 'Кислотность минимальная'] = pd.to_numeric(df.loc[i, 'Кислотность минимальная'])
        df.loc[i, 'Кислотность максимальная'] = pd.to_numeric(df.loc[i, 'Кислотность максимальная'])
        df.loc[i, 'Кислотность итоговая'] = df.loc[i, ['Кислотность минимальная', 'Кислотность максимальная']].mean()
    else:
        df.loc[i,'Кислотность минимальная'] = row
        df.loc[i,'Кислотность максимальная'] = row
        df.loc[i, 'Кислотность минимальная'] = df.loc[i, 'Кислотность минимальная'].replace('%', '')
        df.loc[i, 'Кислотность максимальная'] = df.loc[i, 'Кислотность максимальная'].replace('%', '')
        df.loc[i,'Кислотность итоговая'] = row.replace('%', '')
        df.loc[i, 'Кислотность минимальная'] = df.loc[i, 'Кислотность минимальная'].replace(',', '.')
        df.loc[i, 'Кислотность максимальная'] = df.loc[i, 'Кислотность максимальная'].replace(',', '.')
        df.loc[i, 'Кислотность итоговая'] = df.loc[i, 'Кислотность итоговая'].replace(',', '.')
        df.loc[i, 'Кислотность минимальная'] = pd.to_numeric(df.loc[i, 'Кислотность минимальная'])
        df.loc[i, 'Кислотность максимальная'] = pd.to_numeric(df.loc[i, 'Кислотность максимальная'])
        df.loc[i, 'Кислотность итоговая'] = pd.to_numeric(df.loc[i, 'Кислотность итоговая'])


df.to_excel('khmel.xlsx')