import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get('https://www.bar-beer.ru/blogs/blog/luchshie-kraftovye-pivovarni-v-rossii')
wait = WebDriverWait(driver, 10)
accept_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.btns_was a.button-prod.was_close")))
accept_button.click()
time.sleep(5)
site = driver.page_source
soup = BeautifulSoup(site, 'html.parser')
names_draft = soup.find_all('span', attrs = {'style':'font-size: 12pt; font-family: arial, helvetica, sans-serif;'})
names = []
for name in names_draft:
    if name.find('strong'):
        names.append(name.find('strong').get_text(strip=True))
names = names[::2]
with open("brewery_names.txt", "w") as file:
    file.write(",".join(names))g