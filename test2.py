#coding=utf-8
from selenium import webdriver
import os
import shutil
import time
import re
import traceback
import pymysql
path = "E:\\python\\nothing\\"
replacePath = "E:\\python\\test\\"
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='wangboshun', db='down_list', charset='utf8', cursorclass = pymysql.cursors.DictCursor)
cursor = conn.cursor()  

#做一个等待的通用方法
def sleep(sec=9):
    time.sleep(sec)

profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.dir', 'E:\\python\\nothing\\')
profile.set_preference('browser.download.folderList', 2)
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream')

driver = webdriver.Firefox(executable_path = 'E:\\python\\geckodriver.exe', firefox_profile=profile)

driver.get('http://www.baidu.com/') #+obj['url']

# driver.findElement(By.xpath("//span[contains(text(),'hello')]"))  包含匹配
# driver.findElement(By.xpath("//span[text()='新闻']"))     绝对匹配
driver.implicitly_wait(6)
# alllist = os.listdir(replacePath)
# print(len(alllist), 123)
spl = 'sdsasdf.aa.aa'
try:
    aa,bb = spl.split(".")
except Exception as e:
    print('err',str(Exception))
    print('err',str(e))
url = driver.current_url      

if 'http://www.baidu.com' not in url:
    print(112, url)
# driver.close()