#coding=utf-8
from selenium import webdriver
import os
import shutil
import time
import datetime
import re
import pymysql
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='wangboshun', db='down_list', charset='utf8', cursorclass = pymysql.cursors.DictCursor)
cursor = conn.cursor()
#做一个等待的通用方法
def sleep(sec=9):
    time.sleep(sec)

# profile = webdriver.FirefoxProfile()
# profile.set_preference('browser.download.dir', 'E:\\project\\python\\nothing\\')
# profile.set_preference('browser.download.folderList', 2)
# profile.set_preference('browser.download.manager.showWhenStarting', False)
# profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream')

# driver = webdriver.Firefox(executable_path = 'E:\\project\\python\\geckodriver.exe', firefox_profile=profile)
ulList = [
    {'url': 'http://s8bar.com/forum-307-1.html', 'name': 'wumavideo', 'type': 'video'},
    {'url': 'http://s8bar.com/forum-180-1.html', 'name': 'sanjivideo', 'type': 'video'},
    {'url': 'http://s8bar.com/forum-289-1.html', 'name': 'dongmanvideo', 'type': 'video'},
    {'url': 'http://s8bar.com/forum-222-1.html', 'name': 'youmavideo', 'type': 'video'},
    {'url': 'http://s8bar.com/forum-27-1.html', 'name': 'oumeivideo', 'type': 'video'},
    {'url': 'http://s8bar.com/forum-181-1.html', 'name': 'zipaivideo', 'type': 'video'}
]
def getVideo(dList):
    for i in range(len(dList)):
        print(dList[i])
        sleep(1002)    
for i in range(len(ulList)):
    searchData = "SELECT * FROM "+ulList[i]['name']+"detail"
    cursor.execute(searchData)
    results = cursor.fetchall()
    print(type(results))
    getVideo(results)
    sleep(1002)