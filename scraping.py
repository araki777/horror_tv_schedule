import requests
import sys
from time import sleep
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By

# .envファイルを読み込み
load_dotenv()

def LineNotify(message):
    line_notify_token = os.getenv("LINE_TOKEN")
    line_notify_api = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {line_notify_token}"}
    data = {"message": f'{message}'}
    response = requests.post(line_notify_api, data=data, headers=headers)
    print(response.text)


def main():
    # chromeドライバのオプションを設定
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = "/usr/bin/google-chrome"  # もしくは Chrome ブラウザの実行ファイルのパスを指定
    chrome_options.add_argument("--headless")  # ヘッドレスモードで起動する場合
    chrome_options.add_argument("--no-sandbox")  # セキュリティ対策のためのオプション

    # Chromeドライバーのパスを指定
    chrome_driver_path = "./WebDriver/chrome/chromedriver"

    # Chromeドライバーを起動するためのサービスを設定
    chrome_service = webdriver.chrome.service.Service(chrome_driver_path)

    # Chromeドライバーを起動
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    # 整形したデータを入れる配列
    list1 = []
    list2 = []
    list3 = []
    list4 = []

    # ほん怖用の情報
    query1 = "ほんとうにあった怖い話"
    url1 = "https://tv.yahoo.co.jp/search/?q=" + query1 + "&t=3&t=1&a=48"
    driver.get(url1)

    # ページが完全に読み込まれるまで待機
    driver.implicitly_wait(10)  # 最大10秒まで待機

    # seleniumでページからデータを取得
    date_elements1 = driver.find_elements(By.CLASS_NAME, "programListItemDate")
    title_elements1 = driver.find_elements(By.CLASS_NAME, "programListItemTitleLink")

    if (date_elements1 == None or title_elements1 == None):
        pass
    else:
        for date in date_elements1:
          list1.append(' '.join(date.text.split('\n')))

        for title in title_elements1:
          list2.append(title.text)

    # 世にきみょ用の情報
    query2 = "世にも奇妙な物語"
    url2 = "https://tv.yahoo.co.jp/search/?q=" + query2 + "&t=3&t=1&a=48"
    driver.get(url2)

    # ページが完全に読み込まれるまで待機
    driver.implicitly_wait(10)  # 最大10秒まで待機

    # seleniumでページからデータを取得
    date_elements2 = driver.find_elements(By.CLASS_NAME, "programListItemDate")
    title_elements2 = driver.find_elements(By.CLASS_NAME, "programListItemTitleLink")

    if (date_elements2 == None or title_elements2 == None):
        pass
    else:
      for date in date_elements2:
        list3.append(' '.join(date.text.split('\n')))

      for title in title_elements2:
        list4.append(title.text)

    # データが取得できなかった場合に処理を終了する
    if (len(list1) == 0 and len(list2) == 0 and len(list3) == 0 and len(list4) == 0):
        sys.exit()
    else:
        pass

    # ほん怖のデータがあった場合
    if (len(list1) > 0):
        # ほん怖の履歴ファイルからデータを取得
        f = open('strange.txt', 'r')
        f_old = f.read()
        list_old = f_old.splitlines()
        set_old1 = set(list_old)
        f.close()

        # 新しいデータを入れる配列
        new_list1 = []

        # ほん怖の履歴ファイルと取得したデータを比べる
        for item1, item2 in zip(list1, list2):
            combined_string = f"{item1} {item2}"
            new_list1.append(combined_string)

        set_new1 = set(new_list1)

        set_dif1 = set_new1 - set_old1

        if len(set_dif1) == 0:
            sys.exit()

        else:
            list_now = list(set_dif1)
            list_now.sort()

            for L in list_now:
              message = "新しい番組情報です\n\n" + L
              LineNotify(message)
              sleep(3)

        f = open('horror.txt', 'w')
        for x in list_now:
          f.write(str(x)+"\n")
        f.close()
    else:
        pass

    # 世にきみょのデータがあった場合
    if (len(list3) > 0):
        # 世にきみょの履歴ファイルからデータを取得
        f = open('horror.txt', 'r')
        f_old = f.read()
        list_old = f_old.splitlines()
        set_old2 = set(list_old)
        f.close()

        # 新しいデータを入れる配列
        new_list2 = []

        # 世にきみょの履歴ファイルと取得したデータを比べる
        for item3, item4 in zip(list3, list4):
            combined_string = f"{item3} {item4}"
            new_list2.append(combined_string)

        set_new2 = set(new_list2)

        set_dif2 = set_new2 - set_old2

        if len(set_dif2) == 0:
            sys.exit()

        else:
            list_now = list(set_dif2)
            list_now.sort()

            for L in list_now:
              message = "新しい番組情報です\n\n" + L
              LineNotify(message)
              sleep(3)

        f = open('strange.txt', 'w')
        for x in list_now:
          f.write(str(x)+"\n")
        f.close()
    else:
        pass

    # ブラウザを閉じる
    driver.quit()


if __name__ == "__main__":
    main()