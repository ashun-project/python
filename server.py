#coding=utf-8
from selenium import webdriver
import os
import shutil
import time
import re
import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='wangboshun', db='down_list', charset='utf8', cursorclass = pymysql.cursors.DictCursor)
cursor = conn.cursor()
num = 1
computNum = 1
path = "E:\\python\\nothing\\"
replacePath = "E:\\python\\test\\"

#* 
    # Python用法
        #print (driver.page_source)                   // 打印demo
        #print (ele.get_attribute('innerHTML'))       // 打印某个元素
        #time.sleep(num)                              // 停止等待多少时间，需要引入 import time
        #if 'au' in a:                                // 同等于js的indexOf
        # import pdb # pdb.set_trace()                // 同等于debugger n往下执行
    #selenium用法    
        # driver.close()                                  // 关闭浏览器
        # driver.implicitly_wait(6)                       // 隐形等待6秒 (智能等待以后换成这种  需要测试)
        # driver.page_source                              // 打印demo
        # driver.find_element_by_partial_link_text('132') // 获取a标签的text含有123的属性

        # 操作没有出现在窗口的元素
            # from selenium.webdriver.common.action_chains import ActionChains
            # action = ActionChains(driver)
            # action.move_to_element(a[i]).click().perform()

        # Chrome驱动    
            # Browser ='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe' // 驱动路径
            # os.environ["webdriver.chrome.driver"] = Browser                              // 设置环境变量
            # 文件下载配置
                # options = webdriver.ChromeOptions()  
                # prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'E:\\python\\nothing\\'}
                # options.add_experimental_option('prefs', prefs) 
            # driver = webdriver.Chrome(
                # Browser,                     // 驱动配置
                # chrome_options=options      // 下载配置  
            #)
        # fireFox
            # 文件下载
                # profile = webdriver.FirefoxProfile()
                # profile.set_preference('browser.download.dir', 'E:\\python\\nothing\\')
                # profile.set_preference('browser.download.folderList', 2)
                # profile.set_preference('browser.download.manager.showWhenStarting', False)
                # profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream')

            # driver = webdriver.Firefox(
                # executable_path = 'E:\\python\\geckodriver.exe',   // 驱动路径
                # firefox_profile=profile                            // 下载配置               
            #)    
    # sql
        # conn.escape_string()  // sql对HTML转义
        # cursor.close()        // 关闭游标    
#*

#做一个等待的通用方法

profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.dir', 'E:\\python\\nothing\\')
profile.set_preference('browser.download.folderList', 2)
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream')
driver = webdriver.Firefox(executable_path = 'E:\\python\\geckodriver.exe', firefox_profile=profile)

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
                shutil.copyfile(oldname,replacePath + name + '.' + bb)
                os.remove(oldname)
                computNum = 0
    else:
        if 'http://www.s8bar.com' in driver.current_url:
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
        if os.path.exists('E:\\python\\nothing'):
            try:
                shutil.rmtree('E:\\python\\nothing')  
                os.mkdir('E:\\python\\nothing')
            except Exception as e:
                print('操作文件失败---', e)   
        else:
            os.mkdir('E:\\python\\nothing')
        print('下载----',url)    
        driver.execute_script("document.location.href=arguments[0]", url)
        sleep(3)
        checkOs(currentTime)
     
def getListDetail(arr):
    for i in range(len(arr)):
        if arr[i]['url']:
            try:
                print('页面----',arr[i]['url'])   
                driver.execute_script("document.location.href=arguments[0]", arr[i]['url'])
                driver.implicitly_wait(6)
                sleep(2)
            except Exception as e:
                print('获取详情是出错-------', e)
            else:
                try:
                    cont = driver.find_element_by_xpath('//*[@id="postlist"]/div').find_element_by_class_name('pcb')
                    contHtml = cont.get_attribute('innerHTML')
                    currentTime = int(time.time())
                except Exception as e:
                    print('获取详情内容时出错', e)
                else:
                    addList = "INSERT INTO sanjilist(createTime,url,title,img)values('%d','%s','%s','%s')" % (currentTime,arr[i]['url'],arr[i]['txt'],arr[i]['img'])
                    addDetail = "INSERT INTO sanjidetail(createTime, url, content)values('%d','%s','%s')" % (currentTime,arr[i]['url'], conn.escape_string(contHtml))
                    searchData = "SELECT * FROM sanjilist WHERE title = '%s'" % (arr[i]['txt'])
                    try:
                        cursor.execute(searchData)
                        results = cursor.fetchall()
                        if len(results) <= 0:
                            cursor.execute(addList)
                            cursor.execute(addDetail)
                    except Exception as e:
                        print('执行数据操作出错', e)
                    else:
                        # cursor.close()
                        if len(results) <= 0:
                            conn.commit()
                            getOs(cont, currentTime)
        else:
            print ('url not true')
    # getPage()
    #记得关闭selenium  1天后再次调用init
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
def getPage():
    global num
    sleep(3)
    url = 'http://www.s8bar.com/forum-234-'+ str(num) +'.html'
    try:
        driver.execute_script("document.location.href=arguments[0]", url)
    except Exception as e:
        print('getPage------出错', e)
        getPage()
    else:
        num = num + 1 
        driver.implicitly_wait(6)
        sleep(2)
        geUrltList()
def init():
    try:
        driver.get('http://www.s8bar.com/') #+obj['url']
        driver.find_element_by_id('goin').click()
        driver.find_element_by_id('ls_username').send_keys('sexlookashun') #sexlookashun,ashun6
        driver.find_element_by_id('ls_password').send_keys('ashun666')
        driver.find_element_by_class_name('mem_login').click()
        driver.implicitly_wait(6)
    except Exception as e:
        print('init-------出错', e)
        init()
    else:    
        getPage()    
if __name__ == "__main__": 
    init()
# getListDetail('http://www.s8bar.com/thread-9227434-1-1.html')
# driver.close()