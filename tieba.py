#coding=utf-8
from selenium import webdriver
import os
import shutil
import time
import re
import pymysql
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='ashun666', db='down_list', charset='utf8', cursorclass = pymysql.cursors.DictCursor)
cursor = conn.cursor()  

#做一个等待的通用方法
def sleep(sec=9):
    time.sleep(sec)

driver = webdriver.Firefox()

# driver.get('http://www.baidu.com/') #+obj['url']
# sleep(1)
# driver.find_element_by_id('u1').find_element_by_class_name('lb').click()
# sleep(1)
# driver.find_element_by_id('TANGRAM__PSP_10__footerULoginBtn').click()
# sleep(1)
# driver.find_element_by_id('TANGRAM__PSP_10__userName').send_keys('13952470578')
# driver.find_element_by_id('TANGRAM__PSP_10__password').send_keys('ashun666')
# driver.find_element_by_class_name('TANGRAM__PSP_10__submit').click()
# print(10)
# sleep(60)
# cookies = driver.get_cookies()
# print(cookies)
# driver.get("http://www.baidu.com")
# bdUss = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
# bdussCookie = new Cookie("BDUSS","GhPVE40ci1sRDlnZnY0M2hORHlOVVlZMHVhdkJyRzUyajFzVVllc2x-MzU4TWRiQVFBQUFBJCQAAAAAAAAAAAEAAACB0tnSYXNodW5fNTIwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPljoFv5Y6BbZ")
# bduidCookie = new Cookie("BAIDUID","E2668A0FDBA51636A07481E678D4F108:FG=1")
# driver.manage().addCookie(bduidCookie)
# driver.manage().addCookie(bdussCookie)

# driver.get("http://www.baidu.com")
# driver.execute_script("document.location.href=arguments[0]", 'http://google.com')
# sleep(2)


driver.get("https://www.baidu.com")

# 添加Cookie
driver.add_cookie({'name':'BAIDUID','value':'E2668A0FDBA51636A07481E678D4F108:FG=1'})
driver.add_cookie({'name':'BDUSS','value':'GhPVE40ci1sRDlnZnY0M2hORHlOVVlZMHVhdkJyRzUyajFzVVllc2x-MzU4TWRiQVFBQUFBJCQAAAAAAAAAAAEAAACB0tnSYXNodW5fNTIwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPljoFv5Y6BbZ'})

# 刷新页面
driver.refresh()

# 获取登录用户名并打印；
username = driver.find_element_by_class_name("user-name").text
print(username)

#关闭浏览器
# driver.quit()


