from flask import Flask
from selenium import webdriver
app = Flask(__name__)

# @app.route('/hosts/')
# @allow_cross_domain   #调用函数方法
@app.route('/', methods=['GET'])
def ping_pong():
    driver = webdriver.PhantomJS(executable_path='E:\\ashun-project\\python\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
    driver.get('http://www.baidu.com')
    print (driver.page_source)
    return driver.page_source     #（jsonify返回一个json格式的数据）
if __name__ == '__main__':
    app.run()