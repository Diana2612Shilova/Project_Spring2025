from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
driver = webdriver.Chrome()
driver.get('https://www.avito.ru/moskva/kommercheskaya_nedvizhimost/sdam-ASgBAgICAUSwCNRW')
wait = WebDriverWait(driver, 10)
checkbox_label = wait.until(EC.element_to_be_clickable((By.XPATH, '//label[@role="checkbox"]//span[contains(text(), "Производство")]')))
checkbox_label.click()
time.sleep(10)
area_from = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@data-marker="params[1243]-from/input"]')))
for char in '400':
    area_from.send_keys(char)
    time.sleep(1)
area_to = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@data-marker="params[1243]-to/input"]')))
for char in '1000':
    area_to.send_keys(char)
    time.sleep(1)
time.sleep(1)
button = driver.find_element(By.XPATH, "//button[@data-marker='search-filters/submit-button']//span")
button.click()
time.sleep(1)
price_elements = driver.find_elements(By.XPATH, "//p[@data-marker='item-price']//strong/span")
address_elements = driver.find_elements(By.XPATH, "//div[@class='geo-root-NrkbV']//span[1]")
addresses = [address_element.text for address_element in address_elements]
addresses1 = [item for item in addresses if item != '']
prices = [element.text for element in price_elements]
prices = [price.split('₽')[0] for price in prices]
prices = [price.replace(' ', '') for price in prices]
df = pd.DataFrame()
link_elements = driver.find_elements(By.CSS_SELECTOR, 'a[data-marker="item-title"]')
titles = [element.get_attribute("title") for element in link_elements]
hrefs = [element.get_attribute("href") for element in link_elements]
df['Название'] = titles
df['Ссылка'] = hrefs
df['Адрес'] = addresses1
df['Стоимость в месяц, руб.'] = prices
df.to_csv('rent.csv', encoding='utf-8')
