#coding=utf-8

from selenium import webdriver
import os
import shutil
import time
import datetime
import re
import pymysql
import pdb


num = 1 #530
driver = ''
conn = ''
cursor = ''
exePath = "/Users/ashun/project/python/geckodriver"

def getDriver():
    global driver
    global conn
    global cursor
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='ashun666', db='vip', charset='utf8', cursorclass = pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    driver = webdriver.Firefox(executable_path = exePath)

#做一个等待的通用方法
def sleep(sec=9):
    time.sleep(sec)

def getListDetail(arr):
    for i in range(len(arr)):
        if arr[i]['url']:
            try:
                driver.execute_script("document.location.href=arguments[0]", arr[i]['url'])
                driver.implicitly_wait(6)
            except Exception as e:
                print('get-detail-wrong====', e)
            else:
                try:
                    video = driver.find_element_by_id('content').find_element_by_tag_name('video').get_attribute('src')
                    currentTime = int(time.time())
                except Exception as e:
                    print('get-detail-cont-wrong=====', e)
                else:
                    addList = "INSERT INTO list(createTime,url,title,img)values('%d','%s','%s','%s')" % (currentTime, arr[i]['url'], arr[i]['title'], arr[i]['img'])
                    addDetail = "INSERT INTO defDetail(createTime, url, title, video)values('%d','%s','%s','%s')" % (currentTime,arr[i]['url'], arr[i]['title'], video)
                    searchData = "SELECT * FROM list WHERE title = '%s'" % (arr[i]['title'])
                    try:
                        cursor.execute(searchData)
                        results = cursor.fetchall()
                        if len(results) <= 0:
                            cursor.execute(addList)
                            cursor.execute(addDetail)
                    except Exception as e:
                        print('execute-data-wrong===', e)
                    else:
                        if len(results) <= 0:
                            conn.commit()
                            sleep(3)
        else:
            print ('url not true') 

def geUrltList ():
    try:
        result = driver.find_elements_by_css_selector(".update_area_lists > .i_list")
    except Exception as e:
        print('geUrltList====', e)
        sleep(86400)
        init()
    else: 
        arr = []
        try:
            for i in range(len(result)):
                img = result[i].find_element_by_class_name('waitpic').get_attribute('src')
                url = result[i].find_element_by_class_name('meta-title').get_attribute('href')
                title = result[i].find_element_by_class_name('meta-title').get_attribute('text')
                arr.append({'url': url, 'title': title, 'img': img})
        except Exception as e:
            print('get-list-wrong=======', e)
            sleep(10)
            geUrltList()
        else:
            sleep(3)
            getListDetail(arr)
def getPage():
    global num
    try:
        driver.execute_script("document.location.href=arguments[0]", '/page/'+str(num))
    except Exception as e:
        print('getPage----wrong', e)
        sleep(10)
        # getPage()
    else:
        driver.implicitly_wait(3)
        sleep(2)
        geUrltList()
        num -= 1
        if num == 0:
            num = 1
            tom = datetime.date.today() + datetime.timedelta(days=1)
            twelve = datetime.time(3,0,0)
            tomTwelve = datetime.datetime.combine(tom, twelve)
            tomTwelveSec = time.mktime(time.strptime(str(tomTwelve), '%Y-%m-%d %H:%M:%S'))
            currentT = time.time()
            print('end=====') 
            driver.quit()
            conn.close()
            cursor.close()
            sleep(int(tomTwelveSec - currentT))
            # sleep(10)
            init()
        else:
            getPage()
            
def getInsidePage():
    try:
        url = driver.find_element_by_xpath('//*/h2/a').get_attribute('href')
        print(url, '1-------')
        driver.execute_script("document.location.href=arguments[0]", url)
    except Exception as e:
        print('init-------wrong', e)
        sleep(10)
        getInsidePage()
    else:
        driver.implicitly_wait(6)
        sleep(3)
        getPage()    
def init():
    try:
        getDriver()
        driver.get('https://51xiaoluoli.com')
    except Exception as e:
        print('init-------wrong', e)
        sleep(10)
        init()
    else:
        driver.implicitly_wait(6)
        getInsidePage()
if __name__ == "__main__":
    init() 