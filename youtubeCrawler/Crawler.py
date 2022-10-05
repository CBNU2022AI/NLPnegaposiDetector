
"""

@author 최제현
@date 2022/09/21

유투브 댓글 크롤러

본인 chrome 버전에 맞는 chrome driver 설치됨
"""

from selenium import webdriver
from datetime import datetime
from dateutil.relativedelta import relativedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from youtubeCrawler.fixedQueue import fixedQueue

import time
import re

import pandas as pd
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from pymongo import MongoClient

class Crawler:


    # mongo db 연결
    def connectMongo(self):
        client = MongoClient(host='192.168.35.72', port=27021)

        # db select
        db = client['negaposiSelector']


        return db

    def keywordCrawling(self, keyword):
        keyword.replace(" ", "+")
        db = self.connectMongo()
        data_list = []
        hrefList = []
        # 드라이버 자동설치
        driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
        hrefList = self.hrefCrawling(keyword, driver)

        self.insertHref(hrefList, db)
        print("href insert end")

        collection = db['youtubehref']
        hrefJson = collection.find()

        for json in hrefJson:
            if json["isParsed"] == False:
                href = json["href"]
                commentList = self.commentCrawling(driver, href)
                self.insertComment(commentList, db)
                myquery = { "id": json["_id"] }
                newvalues = { "$set": { "isParsed": True } }
                collection.update_one(myquery, newvalues)
                print(json["href"]+"done\n")

        driver.close()
        print("keyword crawling 끝.")

    def hrefCrawling(self, keyword, driver):

        driver.get("https://www.youtube.com/results?search_query=" + keyword)
        driver.implicitly_wait(3)
        time.sleep(3)

        aTagList = []
        hrefList = []
        hrefJsonList = []


        htmlSource = driver.page_source
        html = BeautifulSoup(htmlSource, 'html.parser')

        aTagList = html.findAll('a', {'class' : "yt-simple-endpoint style-scope ytd-video-renderer"})

        htmlSource = driver.page_source
        html = BeautifulSoup(htmlSource, 'html.parser')

        aTagList = html.findAll('a', {'class' : "yt-simple-endpoint style-scope ytd-video-renderer"})



        print("stub")

        last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

        queue = fixedQueue()
        queue.maxSize = 50
        queueCount = 0

        while True:
            # Scroll 내리기
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

            # Scroll Height를 가져오는 주기
            time.sleep(0.1)
            new_page_height = driver.execute_script("return document.documentElement.scrollHeight")

            # Queue가 꽉 차는 경우 스크롤 내리기 종료
            if(queueCount > queue.maxSize):
                break

            # 첫 Loop 수행 (Queue가 비어있는 경우) 예외 처리
            if(queue.isEmpty()) :
                queue.enqueue(new_page_height)
                queueCount += 1

            # Queue에 가장 먼저 들어온 데이터와 새로 업데이트 된 Scroll Height를 비교함
            # 같으면 그대로 Enqueue, 다르면 Queue의 모든 Data를 Dequeue 후 새로운 Scroll Height를 Enqueue 함.
            else :
                if(queue.peek() == new_page_height) :
                    queue.enqueue(new_page_height)
                    queueCount += 1
                else :
                    queue.enqueue(new_page_height)
                    for z in range(queueCount) :
                        queue.dequeue()
                    queueCount = 1
        htmlSource = driver.page_source
        html = BeautifulSoup(htmlSource, 'html.parser')

        aTagList = html.findAll('a', {'class' : "yt-simple-endpoint style-scope ytd-video-renderer"})

        for a in aTagList:
            hrefList.append(a.attrs["href"])

        htmlSource = driver.page_source
        html = BeautifulSoup(htmlSource, 'html.parser')

        aTagList = html.findAll('a', {'class' : "yt-simple-endpoint style-scope ytd-video-renderer"})

        for a in aTagList:
            newJson = {
                "keyword" : keyword,
                "href" : a.attrs["href"],
                "title" : a.attrs["title"],
                "isParsed" : False
            }
            hrefJsonList.append(newJson)

        return hrefJsonList

    def commentCrawling(self, driver, href):

        dataList = []
        driver.get("https://www.youtube.com"+href)
        now = datetime.now()

        time.sleep(3)
        #       댓글스크롤 구간
        #down the scroll-
        # body = driver.find_element(By.NAME, 'body')
        last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

        queue = fixedQueue()
        queue.maxSize = 50
        queueCount = 0

        while True:
            # Scroll 내리기
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

            # Scroll Height를 가져오는 주기
            time.sleep(0.1)
            new_page_height = driver.execute_script("return document.documentElement.scrollHeight")

            # Queue가 꽉 차는 경우 스크롤 내리기 종료
            if(queueCount > queue.maxSize):
                break

            # 첫 Loop 수행 (Queue가 비어있는 경우) 예외 처리
            if(queue.isEmpty()) :
                queue.enqueue(new_page_height)
                queueCount += 1

            # Queue에 가장 먼저 들어온 데이터와 새로 업데이트 된 Scroll Height를 비교함
            # 같으면 그대로 Enqueue, 다르면 Queue의 모든 Data를 Dequeue 후 새로운 Scroll Height를 Enqueue 함.
            else :
                if(queue.peek() == new_page_height) :
                    queue.enqueue(new_page_height)
                    queueCount += 1
                else :
                    queue.enqueue(new_page_height)
                    for z in range(queueCount) :
                        queue.dequeue()
                    queueCount = 1

            # 기존의 Scroll 내리는 방식
            #if new_page_height == last_page_height:
            #    break
            #last_page_height = new_page_height
            #time.sleep(2.0)

        # print ("[PASS] Get all comments of URL")

        html0 = driver.page_source
        html = BeautifulSoup(html0, 'html.parser')



        comments_list = html.select("#contents > ytd-comment-thread-renderer")
        # print (comments_list)


        for commentTag in comments_list:
            #contents of comment
            comment = commentTag.find('div',{'id':'content'}).text
            comment = comment.replace('\n', '')
            comment = comment.replace('\t', '')
            #print(comment)
            youtube_id = commentTag.find('a', {'id': 'author-text'}).text
            youtube_id = youtube_id.replace('\n', '')
            youtube_id = youtube_id.replace('\t', '')
            youtube_id = youtube_id.strip()

            date = commentTag.find('a', { 'class': 'yt-simple-endpoint style-scope yt-formatted-string'}).text

            dateToken = date.split(" ")


            if(dateToken[1].startwith("hour")):
                realDate = now - relativedelta(hours=int(dateToken[0]))
            elif(dateToken[1].startwith("day")):
                realDate = now - relativedelta(days=int(dateToken[0]))
            elif(dateToken[1].startwith("month")):
                realDate = now - relativedelta(months=int(dateToken[0]))
            elif(dateToken[1].startwith("week")):
                realDate = now - relativedelta(weeks=int(dateToken[0]))
            elif(dateToken[1].startwith("year")):
                realDate = now - relativedelta(years=int(dateToken[0]))
            elif(dateToken[1].startwith("minute")):
                realDate = now - relativedelta(minutes=int(dateToken[0]))
            else:
                print("time error")
                print(date)
                realDate = now

            data = {'youtube_id': youtube_id, 'comment': comment, 'date': realDate}
            dataList.append(data)
        return dataList

    def insertHref(self, hrefList, db):

        collection = db['youtubehref']

        collection.insert_many(hrefList)

    def insertComment(self, commentList, db):

        collection = db['youtubecomment']

        collection.insert_many(commentList)



if __name__=="__main__":
    print("키워드 입력 : ")
    keyword = input()
    if keyword != None:
        crawler = Crawler()
        crawler.keywordCrawling(keyword)
