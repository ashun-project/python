#coding=utf-8

from selenium import webdriver
import os
import shutil
import time
import datetime
import re
# import pymysql
import pdb
import random
import requests
import json

driver = ''
num = 0
exePath = "D:\python\chromedriver.exe"
f = open("ug.json")
useragJson = json.load(f)
ugLen = len(useragJson)
ugNum = 0
path = "C:\\Users\\Administrator\\Downloads\\"

def getDriver(proxy):
    global driver
    global ugNum
    alllist = os.listdir(path)
    if alllist:
        for i in alllist:
            try:
                os.remove(path+i)
            except Exception as e:
                print('i的格式不对吗？', e)
    sp = useragJson[ugNum]['title'].split(',')
    # prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server={0}'.format(proxy))
    chrome_options.add_experimental_option("mobileEmulation", {"deviceMetrics": {"width": int(sp[0]), "height": int(sp[1]), "pixelRatio": 3.0},"userAgent": useragJson[ugNum]['id']})
    # chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    ugNum += 1
    if ugNum == ugLen:
        ugNum = 0

#做一个等待的通用方法
def sleep(sec=9):
    time.sleep(sec)

def goRich():
    alist = driver.find_elements_by_xpath("//*[@href]")
    for link in alist:
        if 'https://jump.yuyue006.cn' in link.get_attribute('href'): 
            try:
                driver.execute_script('document.location=arguments[0]', link.get_attribute('href'))
            except Exception as e:
                print('nothing', e)
            else:
                if num > 20:
                    sleep(3)
                    driver.find_element_by_tag_name('body').click()
                else:
                    sleep(1)
        # elif 'http://70e.info' in link.get_attribute('href'):  #麒麟
        #         try:
        #             driver.execute_script('document.location=arguments[0]', link.get_attribute('href'))
        #         except Exception as e:
        #             print('nothing', e)
        #         else:
        #             if num > 30:
        #                 sleep(3)
        #                 driver.find_element_by_tag_name('body').click()
        #             else:
        #                 sleep(1)

def changePage(randomNum):
    try:
        li = driver.find_element_by_id('data_list').find_elements_by_tag_name('li')
        li[random.randint(0, 6)].click()
        driver.implicitly_wait(6)
    except Exception as e:
        print('nothing',e)
    else:
        if randomNum > 7:
            try:
                bo = driver.find_element_by_class_name('ulNumList').find_element_by_tag_name('li')
                driver.execute_script("document.location.href=arguments[0]", bo.find_element_by_tag_name('a').get_attribute('href'))
                driver.implicitly_wait(6)
            except Exception as e:
                print('nothing2',e)
            
def getInsidePage():
    global num
    num += 1
    sleep(1)
    randomNum = random.randint(0,10)
    if randomNum > 3:
        changePage(randomNum)
    sleep(3)
    if (num % 2) == 0:
        goRich()
    if num == 100:
        num = 0     
    print('end')
    driver.quit()
    init()
def init():
    try:
        response = requests.get('http://tq.http.321184.com/index/getapi/vps_get_use_ips?type=1&time=1&um=LSd8UGRPWlMsYTRSMCZwV2YecwJhSV8LYgFZcVICfF0CVH1aeD9dAyYAXSQLU0svByQ=').text
        print(response, '======')
        getDriver(response)
        driver.get('http://www.ym993.top') #http://www.ym993.top
    except Exception as e:
        print('init-------wrong', e)
        sleep(1)
        try:
            driver.quit()
        except Exception as e:
            print('init-nothing', e)
        init()
    else:
        driver.implicitly_wait(6)
        getInsidePage()
if __name__ == "__main__":
    init() 