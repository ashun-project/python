#coding=utf-8
from selenium import webdriver
import os
import shutil
import time
import re
import pymysql

path = "E:\\project\\python\\nothing\\"
path2 = "E:\\project\\python\\nothing"
replacePath = "E:\\project\\python\\"
replacePath2 = "E:\\project\\ashun\\server\\"
exePath = "E:\\project\\python\\geckodriver.exe"
computNum = 1
driver = ''
conn = ''
cursor = ''
tableName = ''
dataType = ''

def getDriver():
    global driver
    global conn
    global cursor
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='wangboshun', db='down_list', charset='utf8', cursorclass = pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.dir', path)
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream,application/zip')
    driver = webdriver.Firefox(executable_path = exePath, firefox_profile=profile)

#做一个等待的通用方法
def sleep(sec=9):
    time.sleep(sec)

def checkOs(currentTime):
    global computNum
    name = str(currentTime)
    print('1-----------------------',name)
    alllist = os.listdir(path)
    if alllist:
        for i in alllist:
            print(i)
            try:
                aa,bb = i.split(".")
            except Exception as e:
                print('i的格式不对吗？', e)
            else:
                os.rename(path+i, path + name + '.' + bb)
                oldname =  path + name + '.' + bb
                shutil.copyfile(oldname,replacePath+tableName+'\\' + name + '.' + bb)
                shutil.copyfile(oldname,replacePath2+tableName+'\\' + name + '.' + bb)
                os.remove(oldname)
                computNum = 0
    else:
        if 'http://s8bar.com' in driver.current_url:
            if (computNum < 180):
                sleep(1)
                computNum += 1
                checkOs(currentTime)
            else:
                computNum = 0   
        else:
            computNum = 0    

def getOs(cont,currentTime):
    succ = 'fs'
    js = "var divEles=arguments[0].children;var txt='';eachList(divEles);function eachList(data){for(var i=0;i<data.length;i++){var found=false;if(data[i].firstChild){txt=data[i].firstChild.nodeValue||'';}else{txt=data[i].innerText||'';};if(txt.indexOf('下载次数')>-1){var ev=data[i].parentNode;var child=ev.getElementsByTagName('a');var hf='';var cla='';for(var j=0;j<child.length;j++){hf=child[j].getAttribute('href');cla=child[j].getAttribute('class')||'';if(hf.indexOf('forum.php?mod')>-1&&cla.indexOf('xw1')<0){child[j].setAttribute('id','my-set-id');found=true;break;};};};if(!found){var childList=data[i].children;eachList(childList);};};};"
    driver.execute_script(js,cont)
    sleep(1)
    try:
        ev = driver.find_element_by_id('my-set-id')
    except Exception as e:
        print('获取id出错---', e)
    else:
        url = ev.get_attribute('href')
        if os.path.exists(path2):
            try:
                shutil.rmtree(path2)  
                os.mkdir(path2)
            except Exception as e:
                print('操作文件失败---', e)   
        else:
            os.mkdir(path2)
        print('下载----',url)    
        driver.execute_script("document.location.href=arguments[0]", url)
        sleep(3)
        checkOs(currentTime)
     
def getListDetail(arr):
    for i in range(len(arr)):
        if arr[i]['url']:
            try:
                print(tableName,'页面----',arr[i]['url'])   
                driver.execute_script("document.location.href=arguments[0]", arr[i]['url'])
                driver.implicitly_wait(6)
                sleep(3)
            except Exception as e:
                print('获取详情是出错-------', e)
            else:
                try:
                    if dataType == 'video':
                        video = driver.find_element_by_class_name("playerWrap").find_element_by_tag_name('video').get_attribute('src')
                        driver.execute_script("var self = document.getElementsByClassName('playerWrap')[0];self.parentNode.removeChild(self);")
                    cont = driver.find_element_by_xpath('//*[@id="postlist"]/div').find_element_by_class_name('pcb')
                    contHtml = cont.get_attribute('innerHTML')
                    currentTime = int(time.time())
                except Exception as e:
                    print('获取详情内容时出错', e)
                else:
                    if dataType == 'video':
                        addList = "INSERT INTO "+tableName+"list(createTime,url,title,img,type)values('%d','%s','%s','%s','%s')" % (currentTime, arr[i]['url'], arr[i]['txt'], arr[i]['img'], 'all')
                        addDetail = "INSERT INTO "+tableName+"detail(createTime, url, content, video)values('%d','%s','%s','%s')" % (currentTime,arr[i]['url'], conn.escape_string(contHtml), video)
                    else:    
                        addList = "INSERT INTO "+tableName+"list(createTime,url,title,img)values('%d','%s','%s','%s')" % (currentTime,arr[i]['url'],arr[i]['txt'],arr[i]['img'])
                        addDetail = "INSERT INTO "+tableName+"detail(createTime, url, content)values('%d','%s','%s')" % (currentTime,arr[i]['url'], conn.escape_string(contHtml))
                    searchData = "SELECT * FROM "+tableName+"list WHERE title = '%s'" % (arr[i]['txt'])
                    try:
                        cursor.execute(searchData)
                        results = cursor.fetchall()
                        if len(results) <= 0:
                            cursor.execute(addList)
                            cursor.execute(addDetail)
                    except Exception as e:
                        print('执行数据操作出错', e)
                    else:
                        if len(results) <= 0:
                            conn.commit()
                            if dataType == 'download':
                                getOs(cont, currentTime)
        else:
            print ('url not true')                
def geUrltList ():
    try:
        result = driver.find_elements_by_css_selector(".no-b-border > a[class='s xst']")
        targetA = driver.find_elements_by_css_selector(".img_preview_hidden > .cl > a")
    except Exception as e:
        print('geUrltList-----获取元素出错---停止一天查找原因', e)
        sleep(86400)
        init()
    else: 
        arr = []
        try:
            for i in range(len(result)):
                imgStr = ''
                img = ''
                url = result[i].get_attribute('href')
                txt = result[i].text
                if result[i].get_attribute('href') == targetA[i].get_attribute('href'):
                    imgList = targetA[i].find_elements_by_css_selector('.thread-img')
                    for k in range(len(imgList)):
                        # print (imgList[k].get_attribute('src'))
                        if k > 0:
                            imgStr = ','
                        img += imgStr+imgList[k].get_attribute('src')
                else:
                    for j in range(len(targetA)):
                        if result[i].get_attribute('href') == targetA[j].get_attribute('href'):
                            imgList = targetA[j].find_elements_by_css_selector('.thread-img')
                            for k in range(len(imgList)):
                                # print (imgList[k].get_attribute('src'))
                                if k > 0:
                                    imgStr = ','
                                img += imgStr+imgList[k].get_attribute('src')
                            break
                arr.append({'url': url, 'txt': txt, 'img': img})
        except Exception as e:
            print('获取列表出错', e)
            geUrltList()
        else:
            getListDetail(arr)
def getPage(url):
    sleep(5)
    try:
        driver.execute_script("document.location.href=arguments[0]", url)
    except Exception as e:
        print('getPage------出错', e)
        getPage(url)
    else:
        driver.implicitly_wait(6)
        sleep(2)
        geUrltList()
def init():
    try:
        getDriver()
        driver.get('http://s8bar.com/') #+obj['url']
        driver.find_element_by_id('goin').click()
        driver.find_element_by_id('ls_username').send_keys('ashun6') #sexlookashun,ashun6
        driver.find_element_by_id('ls_password').send_keys('ashun666')
        driver.find_element_by_class_name('mem_login').click()
        driver.implicitly_wait(6)
    except Exception as e:
        print('init-------出错', e)
        init()
    else:
        arrUrl = [
            {'url': 'http://s8bar.com/forum-234-1.html', 'name': 'sanji', 'type': 'download'},
            {'url': 'http://s8bar.com/forum-723-1.html', 'name': 'wuma', 'type': 'download'},
            {'url': 'http://s8bar.com/forum-525-1.html', 'name': 'oumei', 'type': 'download'},
            {'url': 'http://s8bar.com/forum-136-1.html', 'name': 'dongman', 'type': 'download'},
            {'url': 'http://s8bar.com/forum-307-1.html', 'name': 'wumavideo', 'type': 'video'}
        ]
        global tableName
        global dataType
        for i in range(len(arrUrl)):
            tableName = arrUrl[i]['name']
            dataType = arrUrl[i]['type']
            getPage(arrUrl[i]['url'])
            sleep(3)
        driver.quit()
        conn.close()
        cursor.close()
        sleep(86400)  #休息一天86400
        init()     
if __name__ == "__main__": 
    init()
# getListDetail('http://s8bar.com/thread-9227434-1-1.html')
# driver.close()