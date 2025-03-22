import requests
import pandas as pd
from bs4 import BeautifulSoup
from requests.compat import urljoin, quote_plus, urlparse, unquote

response = requests.get('https://malt.ru/catalog/solod/karamelnyy/?PAGEN_1=2')
soup = BeautifulSoup(response.text, 'html.parser')
data = []
cards = soup.find_all("div", class_="productCardDescription")
for card in cards:
    title_tag = card.find("a")
    title = title_tag.get_text(strip=True) if title_tag else "Нет названия"

    manufacturer_tag = card.find("div", class_="productCardManufacturer")
    manufacturer = manufacturer_tag.get_text(strip=True) if manufacturer_tag else "Нет данных"

    price_tag = card.find("p", class_="productCardFooterPrice")
    price = price_tag.get_text(strip=True) if price_tag else "Нет цены"

    per_kilo_tag = card.find("div", class_="per-kilo")
    per_kilo = per_kilo_tag.get_text(strip=True) if per_kilo_tag else "Нет данных"

    data.append({
        "Название": title,
        "Производитель": manufacturer,
        "Обычная цена": price,
        "Цена за кг": per_kilo
    })
df = pd.DataFrame(data)


print(df)

df.to_excel("csolod_data2.xlsx", index=False, engine="openpyxl")
