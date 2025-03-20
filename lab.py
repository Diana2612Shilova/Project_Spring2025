from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
data = []
for link in ['https://malt.ru/catalog/solod/?PAGEN_1=1', 'https://malt.ru/catalog/solod/?PAGEN_1=2', 'https://malt.ru/catalog/solod/?PAGEN_1=3', 'https://malt.ru/catalog/solod/?PAGEN_1=4', 'https://malt.ru/catalog/solod/?PAGEN_1=5', 'https://malt.ru/catalog/solod/?PAGEN_1=6']:
    driver = webdriver.Chrome()
    driver.get(link)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    cards = soup.find_all("div", class_="productCardDescription")
    for card in cards:
        title_tag = card.find("a")
        title = title_tag.get_text(strip=True)

        manufacturer_tag = card.find("div", class_="productCardManufacturer")
        manufacturer = manufacturer_tag.get_text(strip=True)

        price_tag = card.find("p", class_="productCardFooterPrice")
        price = price_tag.get_text(strip=True)

        per_kilo_tag = card.find("div", class_="per-kilo")
        per_kilo = per_kilo_tag.get_text(strip=True)

        data.append({
            "Название": title,
            "Производитель": manufacturer,
            "Обычная цена": price,
            "Цена за кг": per_kilo
        })
df = pd.DataFrame(data)
print(df)
df.to_excel('allsolod.xlsx')
