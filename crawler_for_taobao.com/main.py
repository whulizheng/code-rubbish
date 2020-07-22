from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pyquery import PyQuery as pq
import matplotlib.pyplot as plt
from selenium import webdriver
import numpy as np
import requests
import pymongo
import random
import time
import os

item_id = "590396012013"
key = "淘宝"
url = "https://taobao.com/?spm=a230r.1.1581860521.1.5edb1b15UZOEAa"
client = pymongo.MongoClient('localhost')
db = client['taobao']
CHROME_OPTIONS = [
    '--disable-gpu', '–incognito',
    '–user-agent="Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)"'
]
chrome_options = Options()
for i in CHROME_OPTIONS:
    chrome_options.add_argument(i)
driver = webdriver.Chrome(options=chrome_options)

driver.get(url)

wait = WebDriverWait(driver, 60)
wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#J_SiteNavMytaobao')))
driver.find_element_by_css_selector('#J_SiteNavMytaobao').click()
#driver.get("https://login.taobao.com/")
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_QRCodeImg')))
qrcode_img_path = 'https:' + pq(
    driver.find_element_by_css_selector("#J_QRCodeImg").get_attribute(
        'innerHTML'))('img').attr('src')
qrcode_img = requests.get(qrcode_img_path).content
with open('qrcode.png', 'wb') as f:
    f.write(qrcode_img)
os.startfile('qrcode.png')
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'm-userinfo')))
time.sleep(1)
driver.get(url)

driver.get("https://detail.tmall.com/item.htm?id=" + item_id + '#J_Reviews')
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'rate-grid')))
time.sleep(1)
index = 0
while (1):
    try:
        time.sleep(2)
        html = driver.find_element_by_class_name('rate-grid').get_attribute(
            'innerHTML')
        driver.execute_script("window.scrollTo(900, 700);")
        driver.execute_script("window.scrollTo(900, 750);")
        driver.execute_script("window.scrollTo(900, 850);")
        #print(html)
        doc = pq(html)
        items = doc('table tbody tr').items()
        for item in items:
            #print(item)#J_Reviews > div > div.rate-grid > table > tbody > tr:nth-child(1) > td.tm-col-master > div.tm-rate-premiere > div.tm-rate-content > div.tm-rate-fulltxt
            conmente = item(
                '.tm-col-master .tm-rate-content .tm-rate-fulltxt').text()
            data = item('.tm-col-master .tm-rate-date').text()
            conmente.replace(' ', '')
            if (conmente == ""):
                continue
            dic = {"评论": conmente, "时间": data}

            db[item_id].insert_one(dic)
            print(conmente)
        #inputBox.send_keys(key)
        #J_TabBar > li:nth-child(3)
        index += 1
        p = 6
        if (index <= 5):
            p = index + 5
        else:
            p = 11
        tag = "#J_Reviews > div > div.rate-page > div > a:nth-child(" + str(
            p) + ")"
        driver.execute_script("window.scrollTo(900, 750);")
        driver.find_element_by_css_selector(tag).send_keys(Keys.ENTER)
        #wait.until(
        #    EC.element_to_be_clickable((By.CSS_SELECTOR,tag))
        #).click()
        time.sleep(1)
        fake = random.randint(0, 5)
        time.sleep(fake)
        #J_Reviews > div > div.rate-page > div > a:nth-child(6) 1
        #J_Reviews > div > div.rate-page > div > a:nth-child(7) 2
        #J_Reviews > div > div.rate-page > div > a:nth-child(8) 3
        #J_Reviews > div > div.rate-page > div > a:nth-child(9) 4
        #J_Reviews > div > div.rate-page > div > a:nth-child(10) 5
        #J_Reviews > div > div.rate-page > div > a:nth-child(11) 6
        #J_Reviews > div > div.rate-page > div > a:nth-child(11) 8
        #J_Reviews > div > div.rate-page > div > a:nth-child(11) 9
    except:
        time.sleep(1)