import requests
import pandas as pd
import re
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
        'Цена за килограммkhm': price
        })

df = pd.DataFrame(data)
print(df)
df.to_excel('khmel.xlsx')