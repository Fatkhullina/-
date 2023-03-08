from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['main_news']
mvideo = db.mvideo

s = Service('./chromedriver.exe')
options = Options()
options.add_argument('start-maximized')


driver = webdriver.Chrome(service=s, options=options)
driver.get("https://www.mvideo.ru/")


wait = WebDriverWait(driver, 10)
driver. execute_script("window.scrollTo(0, 1300);")


wait = WebDriverWait(driver, 10)
button = driver.find_element(By.XPATH, '//button[contains(@class, "tab-button selected ng-star-inserted")]//following-sibling::button')
button.click()

time.sleep(2)

items = driver.find_element(By.XPATH, '//mvid-shelf-group[contains(@class, "page-carousel-padding ng-star-inserted")]')
list_item = []
for item in items:
    item_info = {}
    link = item.find_element(By.XPATH, './/div[contains(@class, "product-mini-card__name ng-star-inserted")]/../@href')
    name = item.find_element(By.XPATH, './/div[contains(@class, "product-mini-card__name ng-star-inserted")]/div/a/div').text
    price = item.find_element(By.XPATH, './/div[contains(@class, "product-mini-card__price ng-star-inserted")]/mvid-price/div/span').text

    item_info['name'] = name
    item_info['link'] = link
    item_info['price'] = price
    list_item.append(item_info)
    mvideo.insert_one(item_info)

pprint(list_item)