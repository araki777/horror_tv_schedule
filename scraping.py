import requests
from bs4 import BeautifulSoup
import sys
from time import sleep
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By

load_dotenv()


chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = "/usr/bin/google-chrome"  # もしくは Chrome ブラウザの実行ファイルのパスを指定
chrome_options.add_argument("--headless")  # ヘッドレスモードで起動する場合
chrome_options.add_argument("--no-sandbox")  # セキュリティ対策のためのオプション

chrome_driver_path = "./WebDriver/chrome/chromedriver"  # Chromeドライバーのパスを指定

# Chromeドライバーを起動するためのサービスを設定
chrome_service = webdriver.chrome.service.Service(chrome_driver_path)

# Chromeドライバーを起動
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

query = "ほんとにあった怖い話"
url = "https://tv.yahoo.co.jp/search/?q=" + query + "&t=3&t=1&a=48"
driver.get(url)

# ページが完全に読み込まれるまで待機
driver.implicitly_wait(10)  # 最大10秒まで待機

date_elements = driver.find_elements(By.CLASS_NAME, "programListItemDate")
title_elements = driver.find_elements(By.CLASS_NAME, "programListItemTitleLink")

list1 = []
list2 = []

if (date_elements == None or title_elements == None ):
    sys.exit()

else:
    pass


for date in date_elements:
    list1.append(' '.join(date.text.split('\n')))

for title in title_elements:
    list2.append(title.text)

# ブラウザを閉じる
driver.quit()

f = open('news.txt', 'r')
f_old = f.read()
list_old = f_old.splitlines()
set_old = set(list_old)
f.close()

new_list = []

for item1, item2 in zip(list1, list2):
    combined_string = f"{item1} {item2}"
    new_list.append(combined_string)

set_new = set(new_list)

set_dif = set_new - set_old

if len(set_dif) == 0:
    sys.exit()

else:
    list_now = list(set_dif)
    list_now.sort()

    for L in list_now:
        def LineNotify(message):
            line_notify_token = os.getenv("LINE_TOKEN")
            line_notify_api = "https://notify-api.line.me/api/notify"
            headers = {"Authorization": f"Bearer {line_notify_token}"}
            data = {"message": f'{message}'}
            response = requests.post(line_notify_api, data=data, headers=headers)
            print(response.text)
        message = "新しい番組情報です\n\n" + L
        LineNotify(message)
        sleep(3)

f = open('news.txt', 'w')
for x in list_now:
  f.write(str(x)+"\n")
f.close()