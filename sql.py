# -*- coding: <encoding name> -*- 例如，可添加# -*- coding: utf-8 -*-
import pymysql
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='wangboshun', db='down_list', charset='utf8', cursorclass = pymysql.cursors.DictCursor)

cursor = conn.cursor()  
# 创建表
crList = "create table zipaivideolist(createTime int(50), url varchar(100), title varchar(100), img longtext, type varchar(50))"
crDetail = "create table zipaivideodetail(createTime int(50), url varchar(100), content longtext, video varchar(100))"
# 删除表
deList = "DROP TABLE IF EXISTS sanjivideolist"
deDetail = "DROP TABLE IF EXISTS sanjivideodetail"

# 增加数据        
addData = "INSERT INTO LIST(id,name,sex,age)values(30,'san','boy',18)"
# 查询数据
searchData = "SELECT * FROM sanjilist WHERE url = 'boy'"
# 更新数据
updateData = "UPDATE LIST SET SEX = 'girl' WHERE SEX = 'boy'"
# 删除数据
deleteListL = "DELETE FROM sanjilist"
deleteListD = "DELETE FROM sanjidetail"

# 执行
cursor.execute(crList)
cursor.execute(crDetail)
# 执行结果
# results = cursor.fetchall()
# for key in results:
#     print (2,key)
# print (results) 
# 关闭游标
cursor.close()
# 提交更改
conn.commit()