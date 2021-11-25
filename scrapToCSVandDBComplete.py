import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import openpyxl
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import math
import re
import mysql.connector
import _thread
import threading

baseUrl= 'https://www.amazon.de'
url='https://www.amazon.de/gp/bestsellers/?ref_=nav_cs_bestsellers'
scrapeUrl= 'https://www.amazon.de/gp/bestsellers/boost/9418400031/ref=zg_bs_nav_2_9418396031'
TimeoutForCT = 0.05
TimeoutForProd = 2

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="amazon"
)

mycursor = mydb.cursor()


def insertIntoDB(items):
    sql = "INSERT INTO articles (ranking, description, imageUrl, price, averageRating, ratingCount, url, asin, categoryId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    mycursor.executemany(sql, items)

    mydb.commit()

# write csv headers
if os.path.exists('result.csv'):
    os.remove('result.csv')
columns=['ranking', 'description', 'imageUrl', 'price', 'averageRating', 'ratingCount', 'url', 'asin', 'categoryId']
df = pd.DataFrame(columns = columns)
df.to_csv('result.csv', mode='x', index=False, encoding='utf-8-sig')


def insertIntoCSV(items):
    df = pd.DataFrame(items, columns = columns)
    df.to_csv('result.csv', mode='a', header=False, index=False, encoding='utf-8')

def saveInJson(data):
    if os.path.exists('posts.json'):
        os.remove('posts.json')
    f= open('posts.json', 'w', encoding='utf-8-sig')
    f.write(json.dumps(data, ensure_ascii=False))
    f.close()
    print('Saved successfully into json!')

def savesql(items):
    sql = "INSERT INTO categorys (categoryId, parentId, description, url) VALUES (%s, %s, %s, %s)"
    mycursor.executemany(sql, items)
    mydb.commit()

class BestSellerScraper():
    #this is for making driver
    def __init__(self):
        self.threadFlag= 0
    def headlessDriver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(f"--window-size=1920, 900")
        chrome_options.add_argument("--hide-scrollbars")
        driver = webdriver.Chrome(options=chrome_options, executable_path="chromedriver86.exe")
        return driver

    def select_fromJson(self):
        print("now getting deepest urls from Json file!")
        with open('posts.json') as f:
            categorys = json.load(f)
        return categorys

    def select_scrap(self, base_url):
        print('now scrape categorys... and inserting into sql database')
        print('this takes long time, maybe 8+hours..')
        print('after getting all categorys, will be returned all deepset urls and will scrape all products!')
        print('please wait!')
        driver= self.headlessDriver()
        driver.get(base_url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        url1 = soup.find('ul', attrs = {'id':'zg_browseRoot'})
        url1 = url1.find('ul')
        url1 = url1.find_all('li')
        num1 = len(url1)

        category0id = 0
        category1id = 100000
        category2id = 200000
        category3id = 300000
        category4id = 400000
        category5id = 500000
        category6id = 600000
        urls = []
        for url1_num in range(num1):
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
                url3 = url3.find('ul')
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
                            if url4 == None:
                                continue
                            subname = url4.find('a').text.strip()
                            if topname != subname:
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
                                            contine
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

        time.sleep(2)
        saveInJson(urls)
        time.sleep(2)
        return urls
    
    def modifyUrls(self, urls):
        modifiedUrls= []
        modifyNum= 5
        if len(urls)<= modifyNum:
            modifiedUrls.append(urls)
            return modifiedUrls
        else:
            modifiedUrlsLen= int(len(urls)/modifyNum)
            for i in range(modifiedUrlsLen):
                new= []
                for ii in range(modifyNum):
                    new.append(urls[ii+i*modifyNum])
                modifiedUrls.append(new)
            rest= []
            for iii in range(len(urls)- (i+1)*modifyNum):
                rest.append(urls[iii+(i+1)*modifyNum])
            modifiedUrls.append(rest)
        return modifiedUrls

    def urlscrape(self, unitUrl, categoryID, lock):
        driver= self.headlessDriver()
        driver.get(unitUrl)
        time.sleep(TimeoutForProd)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        itemDoms= soup.find_all('li', attrs={'class': 'zg-item-immersion'})
        items=[]
        for itemDom in itemDoms:
            ranking1= 0
            if itemDom.find('span', attrs= {'class': 'zg-badge-text'})!= None:
                ranking1= int(itemDom.find('span', attrs= {'class': 'zg-badge-text'}).text.strip('#'))
            # category1= '_'
            # if soup.find('span', attrs= {'class': 'zg_selected'})!= None:
            #     category1= soup.find('span', attrs= {'class': 'zg_selected'}).text
            description1= '_'
            if itemDom.find('div', attrs= {'class': 'p13n-sc-truncate-desktop-type2 p13n-sc-truncated'})!= None:
                description1= itemDom.find('div', attrs= {'class': 'p13n-sc-truncate-desktop-type2 p13n-sc-truncated'}).text
            imageUrl1= '_'
            if itemDom.find('img')!= None:
                imageUrl1= itemDom.find('img').attrs['src']
            price1= 0
            if itemDom.find('span', attrs= {'class': 'p13n-sc-price'})!= None:
                price1= float(itemDom.find('span', attrs= {'class': 'p13n-sc-price'}).text.strip('\xa0€').replace('.', '', 5).replace(',', '.'))
            averageRating1= 0
            if itemDom.find('span', attrs= {'class': 'a-icon-alt'})!= None:
                averageRating1= float(itemDom.find('span', attrs= {'class': 'a-icon-alt'}).text.split(' ')[0].replace(',', '.'))
            ratingCount1= 0
            if itemDom.find('a', attrs= {'class': 'a-size-small a-link-normal'})!= None:
                ratingCount1= int(itemDom.find('a', attrs= {'class': 'a-size-small a-link-normal'}).text.replace('.', '', 5))
            url1= baseUrl
            if itemDom.find('a', attrs= {'class': 'a-link-normal'})!= None:
                url1+= itemDom.find('a', attrs= {'class': 'a-link-normal'}).attrs['href']
            asin1="_"
            if len(url1.split('/dp/', 1))>=2:
                asin1= url1.split("/dp/", 1)[1].split("/ref=")[0]
            new= (ranking1, description1, imageUrl1, price1, averageRating1, ratingCount1, url1, asin1, categoryID)
            items.append(new)

            # sql = "INSERT INTO articles (ranking, description, imageUrl, price, averageRating, ratingCount, url, asin, category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            # mycursor.execute(sql, new)
            # mydb.commit()
            
        # writing in database
        lock.acquire()
        insertIntoCSV(items)
        insertIntoDB(items)
        lock.release()

        if soup.find('ul', attrs= {'class': 'a-pagination'})!= None:
            if len(soup.find('ul', attrs= {'class': 'a-pagination'}).find_all('li', attrs= {'class': 'a-normal'}))>= 1:
                newPage= soup.find('ul', attrs= {'class': 'a-pagination'}).find('li', attrs= {'class': 'a-normal'}).find('a').attrs['href']
                driver.get(newPage)
                time.sleep(TimeoutForProd)

                soup = BeautifulSoup(driver.page_source, 'html.parser')
                itemDoms= soup.find_all('li', attrs={'class': 'zg-item-immersion'})
                items=[]
                for itemDom in itemDoms:
                    ranking1= 0
                    if itemDom.find('span', attrs= {'class': 'zg-badge-text'})!= None:
                        ranking1= int(itemDom.find('span', attrs= {'class': 'zg-badge-text'}).text.strip('#'))
                    # category1= '_'
                    # if soup.find('span', attrs= {'class': 'zg_selected'})!= None:
                    #     category1= soup.find('span', attrs= {'class': 'zg_selected'}).text
                    description1= '_'
                    if itemDom.find('div', attrs= {'class': 'p13n-sc-truncate-desktop-type2 p13n-sc-truncated'})!= None:
                        description1= itemDom.find('div', attrs= {'class': 'p13n-sc-truncate-desktop-type2 p13n-sc-truncated'}).text
                    imageUrl1= '_'
                    if itemDom.find('img')!= None:
                        imageUrl1= itemDom.find('img').attrs['src']
                    price1= 0
                    if itemDom.find('span', attrs= {'class': 'p13n-sc-price'})!= None:
                        price1= float(itemDom.find('span', attrs= {'class': 'p13n-sc-price'}).text.strip('\xa0€').replace('.', '', 5).replace(',', '.'))
                    averageRating1= 0
                    if itemDom.find('span', attrs= {'class': 'a-icon-alt'})!= None:
                        averageRating1= float(itemDom.find('span', attrs= {'class': 'a-icon-alt'}).text.split(' ')[0].replace(',', '.'))
                    ratingCount1= 0
                    if itemDom.find('a', attrs= {'class': 'a-size-small a-link-normal'})!= None:
                        ratingCount1= int(itemDom.find('a', attrs= {'class': 'a-size-small a-link-normal'}).text.replace('.', '', 5))
                    url1= baseUrl
                    if itemDom.find('a', attrs= {'class': 'a-link-normal'})!= None:
                        url1+= itemDom.find('a', attrs= {'class': 'a-link-normal'}).attrs['href']
                    asin1="_"
                    if len(url1.split('/dp/', 1))>=2:
                        asin1= url1.split("/dp/", 1)[1].split("/ref=")[0]
                    new= (ranking1, description1, imageUrl1, price1, averageRating1, ratingCount1, url1, asin1, categoryID)
                    items.append(new)
                # insert into DB
                lock.acquire()
                insertIntoCSV(items)
                insertIntoDB(items)
                lock.release()

        lock.acquire()
        self.threadFlag+= 1
        lock.release()

    def scrape(self):
        urls=self.select_scrap(url)

        # urls= self.select_fromJson()
        print('all deepest urls already ready!')
        print('now getting all products!')
        modifiedUrls= self.modifyUrls(urls)
        lock = threading.Lock()
        for im in modifiedUrls:
            self.threadFlag= 0
            for i in im:
                categoryID= i['categoryId']
                threading.Thread(target= self.urlscrape, args = (i['url'], categoryID, lock, )).start()
                # _thread.start_new_thread(self.urlscrape, (i[0], categoryID, ))
            while self.threadFlag!= len(im):
                time.sleep(2)
            print('ok! pass thread once')
        print('Done')

if __name__ == '__main__':
    scraper = BestSellerScraper()
    scraper.scrape()