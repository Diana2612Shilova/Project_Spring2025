from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pickle
import re
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.get("https://untappd.com/login")

username = driver.find_element(By.ID, "username")
username.send_keys("yegorlazarev")
password = driver.find_element(By.ID, "password")
password.send_keys("Q1w2e3r4")
time.sleep(10)
login_button = driver.find_element(By.CSS_SELECTOR, "span.button.yellow.submit-btn input")
login_button.click()
pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)
driver.get('https://untappd.com/ZagovorBrewery/beer')
wait = WebDriverWait(driver, 10)
try:
    consent_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.fc-button.fc-cta-consent.fc-primary-button"))
)
    consent_button.click()
except:
    print('continue')
time.sleep(5)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
show_more_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.button.yellow.more-list-items.track-click")))
site = driver.page_source

beer_record = driver.find_element(By.CLASS_NAME, 'beer-item')
beer_link = beer_record.find_element(By.TAG_NAME, 'a').get_attribute('href').split('.com')[-1]
link = f'//p[@class="name"]/a[@href="{beer_link}"]'
buttor_link= driver.find_element(By.XPATH, link)
buttor_link.click()
time.sleep(5)
soup = BeautifulSoup(site, 'html.parser')
reviews = driver.find_elements(By.CLASS_NAME, 'item')
for review in reviews:
    link_to_place =review.find_element(By.CLASS_NAME, 'top').find_element(By.TAG_NAME, 'p').find_elements(By.TAG_NAME, 'a')[-1]
    if '/v/' in link_to_place.get_attribute('href'):
        link_to_place.click()
        time.sleep(1)

        driver.back()
show_more_button.click()
time.sleep(5)

