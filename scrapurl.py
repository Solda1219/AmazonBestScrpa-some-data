import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import mysql.connector
import json

options = Options()
options.headless = False
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(options=options, executable_path="chromedriver86.exe")
#chrome version 86

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="amazon"
)

mycursor = mydb.cursor()

TimeoutForCT = 0.05

test= 6

def saveInJson(data):
    fileName= "posts"+str(test)+".json"
    if os.path.exists(fileName):
        os.remove(fileName)
    f= open(fileName, 'w', encoding='utf-8-sig')
    f.write(json.dumps(data, ensure_ascii=False))
    f.close()
    print('Saved successfully into json!')

def savesql(items):
    sql = "INSERT INTO categorys (categoryId, parentId, description, url) VALUES (%s, %s, %s, %s)"
    mycursor.executemany(sql, items)
    mydb.commit()

class URLScraper():
    def __init__(self):
        self.All_url = "https://www.amazon.de/gp/bestsellers/ref=zg_bs_unv_0_9418401031_2"

    def scrape(self):
        # save_name = 'URL.csv'
        self.select_scrap(self.All_url)

    def select_scrap(self, base_url):
        driver.get(base_url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        url1 = soup.find('ul', attrs = {'id':'zg_browseRoot'})
        url1 = url1.find('ul')
        url1 = url1.find_all('li')
        num1 = len(url1)

        category0id = 0
        category1id = 100005
        category2id = 200077
        category3id = 300393
        category4id = 400755
        category5id = 500362
        category6id = 600896
        urls = []
        for url1_num in range(test-1, test):
            items = []
            sel_url1 = url1[url1_num].find('a').attrs['href']
            driver.get(sel_url1)
            time.sleep(TimeoutForCT)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            url2 = soup.find('ul', attrs = {'id':'zg_browseRoot'})
            if url2 == None:
                time.sleep(10)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                url2 = soup.find('ul', attrs = {'id':'zg_browseRoot'})
            if url2 == None:
                continue
            url2 = url2.find('ul')
            url2 = url2.find('ul')
            url2 = url2.find_all('li')
            num2 = len(url2)
            category1id = category1id + 1
            description = url1[url1_num].find('a').text.strip()
            topname = description
            new = (category1id, category0id, description, sel_url1)
            items.append(new)
            savesql(items)
            
            for url2_num in range(num2):
                items = []
                sel_url2 = url2[url2_num].find('a').attrs['href']
                driver.get(sel_url2)
                time.sleep(TimeoutForCT)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                url3 = soup.find('ul', attrs = {'id':'zg_browseRoot'})
                if url3 == None:
                    time.sleep(10)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    url3 = soup.find('ul', attrs = {'id':'zg_browseRoot'})
                if url3 == None:
                    continue
                url3 = url3.find('ul')
                if url3 == None:
                    continue
                url3 = url3.find('ul')
                if url3 == None:
                    continue
                url3 = url3.find('ul')
                category2id = category2id + 1
                description = url2[url2_num].find('a').text.strip()
                new = (category2id, category1id, description, sel_url2)
                items.append(new)
                savesql(items)
                if url3 != None:
                    url3 = url3.find_all('li')
                    num3 = len(url3)

                    for url3_num in range(num3):
                        items = []
                        if url3[url3_num].find('a') != None:
                            sel_url3 = url3[url3_num].find('a').attrs['href']
                            driver.get(sel_url3)
                            time.sleep(TimeoutForCT)
                            soup = BeautifulSoup(driver.page_source, 'html.parser')
                            url4 = soup.find('ul', attrs = {'id':'zg_browseRoot'})
                            if url4 == None:
                                time.sleep(10)
                                soup = BeautifulSoup(driver.page_source, 'html.parser')
                                url4 = soup.find('ul', attrs = {'id':'zg_browseRoot'})
                            if url4 == None:
                                continue
                            url4 = url4.find('ul')
                            subname = url4.find('a').text.strip()
                            if topname != subname:
                                continue
                            if url4 == None:
                                continue
                            url4 = url4.find('ul')
                            if url4 == None:
                                continue
                            url4 = url4.find('ul')
                            if url4 == None:
                                continue
                            url4 = url4.find('ul')
                            category3id = category3id + 1
                            description = url3[url3_num].find('a').text.strip()
                            new = (category3id, category2id, description, sel_url3)
                            items.append(new)
                            savesql(items)
                            # urltest = url4.find('span')
                            if url4 != None:
                                url4 = url4.find_all('li')
                                num4 = len(url4)

                                for url4_num in range(num4):
                                    items = []
                                    if url4[url4_num].find('a') != None:
                                        sel_url4 = url4[url4_num].find('a').attrs['href']
                                        driver.get(sel_url4)
                                        time.sleep(TimeoutForCT)
                                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                                        url5 = soup.find('ul', attrs = {'id':'zg_browseRoot'})
                                        if url5 == None:
                                            time.sleep(10)
                                            soup = BeautifulSoup(driver.page_source, 'html.parser')
                                            url5 = soup.find('ul', attrs = {'id':'zg_browseRoot'})
                                        if url5 == None:
                                            continue
                                        url5 = url5.find('ul')
                                        if url5 == None:
                                            continue
                                        subname = url5.find('a').text.strip()
                                        if topname != subname:
                                            continue
                                        url5 = url5.find('ul')
                                        if url5 == None:
                                            continue
                                        url5 = url5.find('ul')
                                        if url5 == None:
                                            continue
                                        url5 = url5.find('ul')
                                        if url5 == None:
                                            continue
                                        url5 = url5.find('ul')
                                        category4id = category4id + 1
                                        description = url4[url4_num].find('a').text.strip()
                                        new = (category4id, category3id, description, sel_url4)
                                        items.append(new)
                                        savesql(items)
                                        # urltest = url5.find('span')
                                        if url5 != None:
                                            url5 = url5.find_all('li')
                                            num5 = len(url5)

                                            for url5_num in range(num5):
                                                items = []
                                                if url5[url5_num].find('a') != None:
                                                    sel_url5 = url5[url5_num].find('a').attrs['href']
                                                    driver.get(sel_url5)
                                                    time.sleep(TimeoutForCT)
                                                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                                                    url6 = soup.find('ul', attrs = {'id':'zg_browseRoot'})
                                                    if url6 == None:
                                                        time.sleep(10)
                                                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                                                        url6 = soup.find('ul', attrs = {'id':'zg_browseRoot'})
                                                    if url6 == None:
                                                        continue
                                                    url6 = url6.find('ul')
                                                    if url6 == None:
                                                        continue
                                                    subname = url6.find('a').text.strip()
                                                    if topname != subname:
                                                        continue
                                                    url6 = url6.find('ul')
                                                    if url6 == None:
                                                        continue
                                                    url6 = url6.find('ul')
                                                    if url6 == None:
                                                        continue
                                                    url6 = url6.find('ul')
                                                    if url6 == None:
                                                        continue
                                                    url6 = url6.find('ul')
                                                    if url6 == None:
                                                        continue
                                                    url6 = url6.find('ul')
                                                    category5id = category5id + 1
                                                    description = url5[url5_num].find('a').text.strip()
                                                    new = (category5id ,category4id, description, sel_url5)
                                                    items.append(new)
                                                    savesql(items)
                                                    # urltest = url6.find_all('span')
                                                    if url6 != None:
                                                        url6 = url6.find_all('li')
                                                        num6 = len(url6)

                                                        items = []
                                                        for url6_num in range(num6):
                                                            if url6[url6_num].find('a') != None:
                                                                sel_url6 = url6[url6_num].find('a').attrs['href']
                                                                category6id = category6id + 1
                                                                description = url6[url6_num].find('a').text.strip()
                                                                new = (category6id, category5id, description, sel_url6)
                                                                items.append(new)
                                                                end = {'url':sel_url6, 'categoryId':category6id}
                                                                urls.append(end)
                                                        savesql(items)

                                                    else:
                                                        end = {'url':sel_url5, 'categoryId':category5id}
                                                        urls.append(end)

                                        else:
                                            end = {'url':sel_url4, 'categoryId':category4id}
                                            urls.append(end)

                            else:
                                end = {'url':sel_url3, 'categoryId':category3id}
                                urls.append(end)

                else:
                    end = {'url':sel_url2, 'categoryId':category2id}
                    urls.append(end)
      
        saveInJson(urls)
        print(category1id)
        print(category2id)
        print(category3id)
        print(category4id)
        print(category5id)
        print(category6id)

        # return urls

if __name__ == '__main__':
    scraper = URLScraper()
    scraper.scrape()
