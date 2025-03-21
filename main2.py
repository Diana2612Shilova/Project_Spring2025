from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get('https://jawsbeer.ru/')
time.sleep(2)
button = driver.find_element(By.CSS_SELECTOR, "div.t658__btn_yes")
button.click()
wait = WebDriverWait(driver, 10)
wait.until(EC.invisibility_of_element((By.CSS_SELECTOR, "div.t658__btn_yes")))
beer_menu = driver.find_element(By.XPATH, "//a[@href='/beer']")
beer_menu.click()
wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, ".r.t-rec.t-rec_pt_0.t-rec_pt-res-480_0.nlm113-active-block623074882")))
beers = driver.find_elements(By.CSS_SELECTOR,'.t694__cell.t-card__col.t-card__col_withoutbtn.t-align_center.t-valign_middle')
print(len(beers))
beers_links = [beer.find_element(By.TAG_NAME, "a").get_attribute('href') for beer in beers if beer.find_elements(By.TAG_NAME, "a")]
beers_links = list(set(beers_links))
beers_links.remove('https://macro-salty-chocolate/')
beers_links.append('https://jawsbeer.ru/macro-salty-chocolate/')
print(beers_links)
number =0
beers_dict = []
for link_ in beers_links:
    number+=1
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get(link_)
    time.sleep(2)
    wait.until(EC.invisibility_of_element((By.CSS_SELECTOR, "div.t658__btn_yes")))
    button = driver.find_element(By.CSS_SELECTOR, "div.t658__btn_yes")
    button.click()
    time.sleep(2)
    elements = driver.find_elements(By.XPATH, '//div[contains(@class, "tn-atom")]')
    print()
    for i in range(len(elements) - 1):
        if 'алкоголь' in elements[i].text:
            labels = elements[i].text.split('\n')
            labels = [item for item in labels if item]
            data = elements[i+1].text.split('\n')
            dict_ = dict(zip(labels, data))
    dict_['name'] = link_.split('/')[-1]
    beers_dict.append(dict_)
    if number % 2 == 0:
        df = pd.DataFrame(beers_dict)
        df.to_csv('pivy.csv')