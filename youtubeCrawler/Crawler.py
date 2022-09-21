
"""

@author 최제현
@date 2022/09/21

유투브 댓글 크롤러

"""


from selenium import webdriver
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

crawler = Crawler()