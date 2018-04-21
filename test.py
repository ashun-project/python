#coding=utf-8
from selenium import webdriver
import os
import shutil
import time
import re
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

driver.get('http://www.s8bar.com/') #+obj['url']
driver.find_element_by_id('goin').click()
driver.find_element_by_id('ls_username').send_keys('sexlookashun')
driver.find_element_by_id('ls_password').send_keys('ashun666')
driver.find_element_by_class_name('mem_login').click()
sleep(2)
driver.execute_script("document.location.href=arguments[0]", 'http://www.s8bar.com/thread-9271473-1-1.html')
driver.implicitly_wait(6)
cont = driver.find_element_by_xpath('//*[@id="postlist"]/div')
alist = cont.find_element_by_class_name('pcb')
a = alist.find_elements_by_tag_name('a')

def getOs(a):
    for i in range(len(a)):
        txt = a[i].text
        url = a[i].get_attribute('href')
        if txt[0:3] in '[法国/限制级]艾曼紐 Emmanuelle[MP4/1.89GB]' and 'forum.php?mod' in url:
            print (txt, url)
            driver.execute_script("document.location.href=arguments[0]", url)
            break
    sleep(2) 
    checkOs()    
def checkOs():
    print('1-----------------------')
    alllist = os.listdir(path)
    if alllist:
        for i in alllist:
            aa,bb = i.split(".")
            os.rename(path+i, path+'88.'+bb)
            oldname = path+ '88.' + bb
            shutil.copyfile(oldname,replacePath+'88.'+bb)
            os.remove(oldname)
            print(aa, bb, 456)
    else:
        sleep(1)
        checkOs()
getOs(a)