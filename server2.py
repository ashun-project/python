#coding=utf-8
from selenium import webdriver
import os
import shutil
import time
import datetime
import re
import pymysql

path = "C:\\project\\python\\nothing\\"
path2 = "C:\\project\\python\\nothing"
replacePath = "C:\\project\\python\\"
replacePath2 = "C:\\project\\ashun\\server\\"
exePath = "C:\\project\\python\\geckodriver.exe"
computNum = 1
driver = ''
conn = ''
cursor = ''
tableName = ''
dataType = ''
num = 1

def getDriver():
    global driver
    global conn
    global cursor
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='ashun666', db='xinba', charset='utf8', cursorclass = pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    profile = webdriver.ChromeOptions()
    # profile.set_preference('browser.download.dir', path)
    # profile.set_preference('browser.download.folderList', 2)
    # profile.set_preference('browser.download.manager.showWhenStarting', False)
    # profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream,application/zip')
    driver = webdriver.Chrome(chrome_options=profile)

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
                # shutil.copyfile(oldname,replacePath+tableName+'\\' + name + '.' + bb)
                shutil.copyfile(oldname,replacePath2+tableName+'\\' + name + '.' + bb)
                os.remove(oldname)
                computNum = 0
    else:
        if 'http://s8bar.com' in driver.current_url:
            if (computNum < 180):
                sleep(2)
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
    sleep(2)
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
        if 'http://s8bar.com' in driver.current_url:
            checkOs(currentTime)
        else:  
            print('下载url出错') 
     
def getListDetail(arr):
    for i in range(len(arr)):
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
                    video = driver.find_element_by_class_name("playerWrap").get_attribute('data-normal')
                #     driver.execute_script("var self = document.getElementsByClassName('playerWrap')[0];self.parentNode.removeChild(self);")
                # cont = driver.find_element_by_xpath('//*[@id="postlist"]/div').find_element_by_class_name('pcb')
                # contHtml = cont.get_attribute('innerHTML')
                currentTime = int(time.time())
            except Exception as e:
                print('获取详情内容时出错', e)
            else:
                if dataType == 'video':
                    addList = "INSERT INTO "+tableName+"(create_time,url,title,img,type,video)values('%d','%s','%s','%s','%s','%s')" % (currentTime, arr[i]['url'], arr[i]['txt'], arr[i]['img'], tableName, video)
                    # addDetail = "INSERT INTO "+tableName+"detail(createTime, url, content, video, title)values('%d','%s','%s','%s','%s')" % (currentTime,arr[i]['url'], conn.escape_string(contHtml), video, arr[i]['txt'])
                else:    
                    addList = "INSERT INTO "+tableName+"(create_time,url,title,img)values('%d','%s','%s','%s')" % (currentTime,arr[i]['url'],arr[i]['txt'],arr[i]['img'])
                    # addDetail = "INSERT INTO "+tableName+"detail(createTime, url, content)values('%d','%s','%s')" % (currentTime,arr[i]['url'], conn.escape_string(contHtml))
                try:
                    cursor.execute(addList)
                    # cursor.execute(addDetail)
                except Exception as e:
                    print('执行数据操作出错', e)
                else:
                    conn.commit()
                    if dataType == 'download':
                        getOs(cont, currentTime)
def quchong (arr):
    arr2 = []
    for i in range(len(arr)):
        if (bool(arr[i]['img'] and arr[i]['img'].strip()) and bool(arr[i]['url'] and arr[i]['url'].strip())):
            searchData = "SELECT * FROM "+tableName+" WHERE url = '%s'" % (arr[i]['url'])
            try:
                cursor.execute(searchData)
                results = cursor.fetchall()
                if len(results) <= 0:
                    arr2.append(arr[i])
            except Exception as e:
                print('search err', e)
            if len(arr2) > 10:
                break
    getListDetail(arr2)

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
            quchong(arr)
def getPage(url):
    sleep(3)
    try:
        driver.execute_script("document.location.href=arguments[0]", url)
    except Exception as e:
        print('getPage------出错', e)
        getPage(url)
    else:
        if 'http://s8bar.com' in driver.current_url:
            driver.implicitly_wait(3)
            sleep(2)
            geUrltList()
        else:   
            print('获取getPage的url出错')
            getPage(url)
def section(ulList, second):
    global tableName
    global dataType
    for i in range(len(ulList)):
        tableName = ulList[i]['name']
        dataType = ulList[i]['type']
        getPage(ulList[i]['url'])
        sleep(2)
    driver.quit()
    conn.close()
    cursor.close()
    # if num == 1:
    #     sleep(86400)
    # else:
    #     sleep(5)  #休息一天86400  second
    sleep(second)    
    init()           
def init():
    global num
    try:
        getDriver()
        driver.get('http://s8bar.com/') #+obj['url']
        sleep(3)
        driver.find_element_by_id('goin').click()
        driver.find_element_by_id('ls_username').send_keys('ashun6') #sexlookashun,ashun6
        driver.find_element_by_id('ls_password').send_keys('ashun666')
        driver.find_element_by_class_name('mem_login').click()
        driver.implicitly_wait(6)
    except Exception as e:
        print('init-------出错', e)
        init()
    else:
        if 'http://s8bar.com' in driver.current_url:
            # arrUrl = [
            #     {'url': 'http://s8bar.com/forum-234-'+ str(num) +'.html', 'name': 'sanji', 'type': 'download'},
            #     {'url': 'http://s8bar.com/forum-723-'+ str(num) +'.html', 'name': 'wuma', 'type': 'download'},
            #     {'url': 'http://s8bar.com/forum-525-'+ str(num) +'.html', 'name': 'oumei', 'type': 'download'},
            #     {'url': 'http://s8bar.com/forum-136-'+ str(num) +'.html', 'name': 'dongman', 'type': 'download'}
            # ]
            arrUrl2 = [
                {'url': 'http://s8bar.com/forum-307-'+ str(num) +'.html', 'name': 'wumavideo', 'type': 'video'},
                {'url': 'http://s8bar.com/forum-180-'+ str(num) +'.html', 'name': 'sanjivideo', 'type': 'video'},
                {'url': 'http://s8bar.com/forum-289-'+ str(num) +'.html', 'name': 'dongmanvideo', 'type': 'video'},
                {'url': 'http://s8bar.com/forum-222-'+ str(num) +'.html', 'name': 'youmavideo', 'type': 'video'},
                {'url': 'http://s8bar.com/forum-27-'+ str(num) +'.html', 'name': 'oumeivideo', 'type': 'video'},
                {'url': 'http://s8bar.com/forum-181-'+ str(num) +'.html', 'name': 'zipaivideo', 'type': 'video'},
                {'url': 'http://s8bar.com/forum-142-'+ str(num) +'.html', 'name': 'lingleivideo', 'type': 'video'}
            ]
            tom = datetime.date.today() + datetime.timedelta(days=1)
            twelve = datetime.time(3,0,0)
            tomTwelve = datetime.datetime.combine(tom, twelve)
            tomTwelveSec = time.mktime(time.strptime(str(tomTwelve), '%Y-%m-%d %H:%M:%S'))
            currentT = time.time()
            section(arrUrl2, int(tomTwelveSec - currentT))
            # if dataType == 'download':
            #     tom = datetime.date.today() + datetime.timedelta(days=1)
            #     twelve = datetime.time(3,0,0)
            #     tomTwelve = datetime.datetime.combine(tom, twelve)
            #     tomTwelveSec = time.mktime(time.strptime(str(tomTwelve), '%Y-%m-%d %H:%M:%S'))
            #     currentT = time.time()
            #     # num = num - 1
            #     section(arrUrl2, int(tomTwelveSec - currentT))
            # else:
            #     section(arrUrl, 10)
        else:
            print('init-获取URL出错')
            init()
          
if __name__ == "__main__": 
    init()
# getListDetail('http://s8bar.com/thread-9227434-1-1.html')
# driver.close()