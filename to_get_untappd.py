from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pickle
import re
import pandas as pd
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
show_more_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.button.yellow.more-list-items.track-click")))
site = driver.page_source

beer_record = driver.find_element(By.CLASS_NAME, 'beer-item')
beer_link = beer_record.find_element(By.TAG_NAME, 'a').get_attribute('href').split('.com')[-1]
link = f'//p[@class="name"]/a[@href="{beer_link}"]'
buttor_link= driver.find_element(By.XPATH, link)
buttor_link.click()
time.sleep(5)
soup = BeautifulSoup(site, 'html.parser')
it_ = 0
threshold = 6
while it_ <threshold:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    show_more_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.more_checkins.button.yellow.track-click.more_checkins_logged")))
    show_more_button.click()
    it_+=1
reviews = driver.find_element(By.ID, 'main-stream').find_elements(By.CLASS_NAME, 'item')
places_links = []
print(len(reviews))
for review in reviews:
    checkin = review.find_element(By.CLASS_NAME, 'checkin')
    top_ =checkin.find_element(By.CLASS_NAME, 'top')
    print(top_)
    p_ = top_.find_element(By.TAG_NAME, 'p')
    a_ =p_.find_elements(By.TAG_NAME, 'a')[-1]
    if '/v/' in a_.get_attribute('href'):
        places_links.append(a_.get_attribute('href'))
names, addresses, links, = [],[],[]
number = 0
for places_link in places_links:
    driver.get(places_link)
    pub_html = driver.page_source
    pub_soup = BeautifulSoup(pub_html, 'html.parser')
    names.append(pub_soup.find(class_='venue-name').find('h1').get_text(strip=True).split(' / ')[0].strip())
    addresses.append(pub_soup.find(class_='desktop-meta').get_text(strip=True).split('(Map)')[0].strip())
    links.append(places_link)
    number += 1
    if number % 2 == 0:
        df = pd.DataFrame({'name':names, 'address':addresses, 'link':links})
        df = df.drop_duplicates(subset=df.columns[0])
        df = df[df['name'] != 'Untappd at Home']
        df.to_csv('pubs.csv')
    driver.back()
    time.sleep(2)
