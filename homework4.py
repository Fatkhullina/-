from lxml import html
from pprint import pprint
import requests
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('127.0.0.1', 27017)
db = client['main_news']
news = db.news

url = 'https://news.mail.ru/?_ga=2.20398520.1868349536.1658662853-1082230887.1656517427'
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
response = requests.get(url, headers=headers)


dom = html.fromstring(response.text)

items = dom.xpath('//div[contains(@class, "daynews__item")]')
list_item = []
for item in items:
    item_info = {}

    item_name = item.xpath('.//span[@class="photo__title photo__title_new photo__title_new_hidden js-topnews__notification"]/text()')
    item_source = item.xpath('.//a[contains(@class, "js-topnews__item")]/@href')
    item_data =str(datetime.now().date())

    item_info['name'] = item_name[0].replace('\xa0', ' ')
    item_info['link'] = item_source[0]
    item_info['data'] = item_data



    list_item.append(item_info)
    print()

    news.insert_one(item_info)

pprint(list_item)


