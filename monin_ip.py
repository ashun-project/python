# from selenium import webdriver
# import os
# import random

# exePath = "E:\\ashun-project\\python\\geckodriver.exe"
# proxyIp = "183.129.244.16"
# proxyPort = 20183

# profile = webdriver.FirefoxProfile()
# profile.set_preference("network.proxy.type", 1)
# profile.set_preference("network.proxy.http", proxyIp)
# profile.set_preference("network.proxy.http_port", proxyPort)
# profile.set_preference("network.proxy.ssl", proxyIp)
# profile.set_preference("network.proxy.ssl_port", proxyPort)
# driver = webdriver.Firefox(executable_path = exePath, firefox_profile=profile)
# # driver.get('http://ashun1.com')
# try:
#     driver.get('http://httpbin.org/ip')
# except Exception as e:
#     print('getPage----wrong', e)
# else:
#     print('success')

# from selenium import webdriver
# options = webdriver.ChromeOptions()
# path1 = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
# # options.add_argument('user-agent="MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"') 
# options.add_argument('lang=zh_CN.UTF-8')
# # options.add_argument('user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"')
# driver = webdriver.Chrome(executable_path = path1,chrome_options = options)
# # driver.get('http://httpbin.org/ip')
# driver.get('http://localhost:8989')

from selenium import webdriver
# from selenium.webdriver.common.touch_actionsimportTouchActions


from selenium.webdriver.chrome.options import Options
mobile_emulation = {"deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },"userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"}
chrome_options = Options() 
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

exePath = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
driver = webdriver.Chrome(exePath, chrome_options = chrome_options)
driver.get('http://www.baidu.com')
# driver.execute_script("document.location.href=arguments[0]", 'http://www.baidu.com')
print('打开浏览器')

print('关闭')
