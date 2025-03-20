from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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
for i in range(1,17):
    button = driver.find_element(By.CSS_SELECTOR, f".button{i}")
    time.sleep(1)
    button.click()
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, ".r.t-rec.t-rec_pt_0.t-rec_pt-res-480_0.nlm113-active-block623074882")))
    beers = driver.find_elements(By.CSS_SELECTOR,'.t694__cell.t-card__col.t-card__col_withoutbtn.t-align_center.t-valign_middle')
    print(len(beers))
    for beer in beers:
        print(beer.find_element(By.TAG_NAME, "a").get_attribute('href'))
        beer.click()
        time.sleep(1)
        driver.back()
        time.sleep(1)
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f".button{i}")))
    time.sleep(5)