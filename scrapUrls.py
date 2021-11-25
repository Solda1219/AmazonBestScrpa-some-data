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

def saveInJson(data):
    f= open('posts.json', 'w', encoding='utf-8-sig')
    f.write(json.dumps(data, ensure_ascii=False))
    f.close()
    print('Saved successfully!')

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

        # first stage
        items = []
        for url1_num in range(num1):
            sel_url1 = url1[url1_num].find('a').attrs['href']
            parentid = 0
            url = sel_url1
            description = url1[url1_num].find('a').text.strip()
            new = (parentid, description, url)
            items.append(new)
        sql = "INSERT INTO category (parentid, description, url) VALUES (%s, %s, %s)"
        mycursor.executemany(sql, items)
        mydb.commit()

        # second stage
        categoryid = num1
        items = []
        for url1_num in range(num1):
            sel_url1 = url1[url1_num].find('a').attrs['href']
            driver.get(sel_url1)
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            url2 = soup.find('ul', attrs = {'id':'zg_browseRoot'})
            url2 = url2.find('ul')
            url2 = url2.find('ul')
            url2 = url2.find_all('li')
            num2 = len(url2)

            items = []
            for url2_num in range(num2):
                sel_url2 = url2[url2_num].find('a').attrs['href']
                parentid = url1_num + 1
                description = url2[url2_num].find('a').text.strip()
                url = sel_url2
                new = (parentid, description, url)
                items.append(new)
                categoryid = categoryid + 1
            sql = "INSERT INTO category (parentid, description, url) VALUES (%s, %s, %s)"
            mycursor.executemany(sql, items)
            mydb.commit()

        # third stage
        items = []
        parentid = num1
        parent1id = num1
        parent2id = categoryid
        for url1_num in range(num1):
            sel_url1 = url1[url1_num].find('a').attrs['href']
            driver.get(sel_url1)
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            url2 = soup.find('ul', attrs = {'id':'zg_browseRoot'})
            url2 = url2.find('ul')
            url2 = url2.find('ul')
            url2 = url2.find_all('li')
            num2 = len(url2)
            
            items = []
            for url2_num in range(num2):
                sel_url2 = url2[url2_num].find('a').attrs['href']
                driver.get(sel_url2)
                time.sleep(1)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                url3 = soup.find('ul', attrs = {'id':'zg_browseRoot'})
                url3 = url3.find('ul')
                url3 = url3.find('ul')
                url3 = url3.find('ul')
                parent2id = parent2id + 1
                if url3 != None:
                    url3 = url3.find_all('li')
                    num3 = len(url3)

                    items = []
                    for url3_num in range(num3):
                        if url3[url3_num].find('a') != None:
                            sel_url3 = url3[url3_num].find('a').attrs['href']
                            description = url3[url3_num].find('a').text.strip()
                            url = sel_url3
                            new = (parent2id, description, url)
                            categoryid = categoryid + 1
                            items.append(new)
                        
                    sql = "INSERT INTO category (parentid, description, url) VALUES (%s, %s, %s)"
                    mycursor.executemany(sql, items)
                    mydb.commit()

        # fourth stage
        items = []
        parent3id = categoryid
        for url1_num in range(num1):
            sel_url1 = url1[url1_num].find('a').attrs['href']
            driver.get(sel_url1)
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            url2 = soup.find('ul', attrs = {'id':'zg_browseRoot'})
            url2 = url2.find('ul')
            url2 = url2.find('ul')
            url2 = url2.find_all('li')
            num2 = len(url2)
            
            items = []
            for url2_num in range(num2):
                sel_url2 = url2[url2_num].find('a').attrs['href']
                driver.get(sel_url2)
                time.sleep(1)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                url3 = soup.find('ul', attrs = {'id':'zg_browseRoot'})
                url3 = url3.find('ul')
                url3 = url3.find('ul')
                url3 = url3.find('ul')
                if url3 != None:
                    url3 = url3.find_all('li')
                    num3 = len(url3)

                    items = []
                    for url3_num in range(num3):
                        if url3[url3_num].find('a') != None:
                            sel_url3 = url3[url3_num].find('a').attrs['href']
                            driver.get(sel_url3)
                            time.sleep(1)
                            soup = BeautifulSoup(driver.page_source, 'html.parser')
                            url4 = soup.find('ul', attrs = {'id':'zg_browseRoot'})
                            url4 = url4.find('ul')
                            url4 = url4.find('ul')
                            url4 = url4.find('ul')
                            parent3id = parent3id + 1
                            if url4 != None:
                                url4 = url4.find_all('li')
                                num4 = len(url4)

                                items = []
                                for url4_num in range(num4):
                                    if url4[url4_num].find('a') != None:
                                        sel_url4 = url4[url4_num].find('a').attrs['href']
                                        description = url4[url4_num].find('a').text.strip()
                                        url = sel_url4
                                        new = (parent3id, description, url)
                                        categoryid = categoryid + 1
                                        items.append(new)

                                sql = "INSERT INTO category (parentid, description, url) VALUES (%s, %s, %s)"
                                mycursor.executemany(sql, items)
                                mydb.commit()

        # fifth stage
        # categoryid = 13333
        # parent1id = 39
        # parent2id = 599
        # parent3id = 4344
        items = []
        parent4id = categoryid
        urls = []
        for url1_num in range(num1):
            sel_url1 = url1[url1_num].find('a').attrs['href']
            driver.get(sel_url1)
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            url2 = soup.find('ul', attrs = {'id':'zg_browseRoot'})
            url2 = url2.find('ul')
            url2 = url2.find('ul')
            url2 = url2.find_all('li')
            num2 = len(url2)
            
            items = []
            for url2_num in range(num2):
                sel_url2 = url2[url2_num].find('a').attrs['href']
                driver.get(sel_url2)
                time.sleep(1)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                url3 = soup.find('ul', attrs = {'id':'zg_browseRoot'})
                url3 = url3.find('ul')
                url3 = url3.find('ul')
                url3 = url3.find('ul')
                parent1id = parent1id + 1
                if url3 != None:
                    url3 = url3.find_all('li')
                    num3 = len(url3)

                    items = []
                    for url3_num in range(num3):
                        if url3[url3_num].find('a') != None:
                            sel_url3 = url3[url3_num].find('a').attrs['href']
                            driver.get(sel_url3)
                            time.sleep(1)
                            soup = BeautifulSoup(driver.page_source, 'html.parser')
                            url4 = soup.find('ul', attrs = {'id':'zg_browseRoot'})
                            url4 = url4.find('ul')
                            url4 = url4.find('ul')
                            url4 = url4.find('ul')
                            if url4 != None:
                                url4 = url4.find_all('li')
                                num4 = len(url4)

                                items = []
                                for url4_num in range(num4):
                                    if url4[url4_num].find('a') != None:
                                        sel_url4 = url4[url4_num].find('a').attrs['href']
                                        driver.get(sel_url4)
                                        time.sleep(1)
                                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                                        url5 = soup.find('ul', attrs = {'id':'zg_browseRoot'})
                                        url5 = url5.find('ul')
                                        url5 = url5.find('ul')
                                        url5 = url5.find('ul')
                                        parent4id = parent4id + 1
                                        if url5 != None:
                                            url5 = url5.find_all('li')
                                            num5 = len(url5)

                                            items = []
                                            for url5_num in range(num5):
                                                if url5[url5_num].find('a') != None:
                                                    sel_url5 = url5[url5_num].find('a').attrs['href']
                                                    description = url5[url5_num].find('a').text.strip()
                                                    url = sel_url5
                                                    new = (parent4id, description, url)
                                                    categoryid = categoryid + 1
                                                    items.append(new)
                                                    news = {'url':url, 'categoryId':categoryid}
                                                    urls.append(news)
                                            # saveInJson(urls)

                                            sql = "INSERT INTO category (parentid, description, url) VALUES (%s, %s, %s)"
                                            mycursor.executemany(sql, items)
                                            mydb.commit()

                                        else:
                                            news = {'url':sel_url4, 'categoryId':parent3id}
                                            urls.append(news)

                            else:
                                news = {'url':sel_url3, 'categoryId':parent2id}
                                urls.append(news)

                else:
                    news = {'url':sel_url2, 'categoryId':parent1id}
                    urls.append(news)
      
        saveInJson(urls)

        # return urls

if __name__ == '__main__':
    scraper = URLScraper()
    scraper.scrape()
