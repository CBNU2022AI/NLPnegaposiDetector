
"""

@author 최제현
@date 2022/09/21

유투브 댓글 크롤러

본인 chrome 버전에 맞는 chrome driver 설치됨
"""


from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import pandas as pd
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from pymongo import MongoClient

class Crawler:


    # mongo db 연결
    def connectMongo(self):
        client = MongoClient(host='teamfrankly.kr', port=27021)

        # db select
        db = client['negaposiSelector']
        collection = db['youtube']

        return collection

    def keywordCrawling(self, keyword):
        con = self.connectMongo()

        driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
        driver.get("https://www.youtube.com/?hl=ko&gl=KR")
        driver.implicitly_wait(3)

        time.sleep(1.5)

        driver.execute_script("window.scrollTo(0, 800)")
        time.sleep(3)

print("키워드 입력 : ")
keyword = input()
if keyword != None:
    crawler = Crawler()
    crawler.keywordCrawling(keyword)
