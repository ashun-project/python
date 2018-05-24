#coding=utf-8
from selenium import webdriver
import os
import shutil
import time
import re
import traceback
import pymysql

#做一个等待的通用方法
def sleep(sec=9):
    time.sleep(sec)
Browser ='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe' #// 驱动路径
os.environ["webdriver.chrome.driver"] = Browser                              #// 设置环境变量
driver = webdriver.Chrome(Browser)

driver.get('http://s8bar.com') #+obj['url']

print (12212)