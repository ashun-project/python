# -*- coding: <encoding name> -*- 例如，可添加# -*- coding: utf-8 -*-
import pymysql
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='wangboshun', db='down_list', charset='utf8', cursorclass = pymysql.cursors.DictCursor)

cursor = conn.cursor()  
# 创建表
Student = "create table sanjidetail(createTime int(50), url varchar(100), content longtext)"
# 删除表
deList = "DROP TABLE IF EXISTS sanjilist"
deDetail = "DROP TABLE IF EXISTS sanjidetail"

# 增加数据        
addData = "INSERT INTO LIST(id,name,sex,age)values(30,'san','boy',18)"
# 查询数据
searchData = "SELECT * FROM LIST WHERE sex = 'boy'"
# 更新数据
updateData = "UPDATE LIST SET SEX = 'girl' WHERE SEX = 'boy'"
# 删除数据
deleteListL = "DELETE FROM sanjilist"
deleteListD = "DELETE FROM sanjidetail"

# 执行
# cursor.execute(deleteListL)
cursor.execute(Student)
# 执行结果
# results = cursor.fetchall()
# for key in results:
#     print (2,key)
# print (results) 
# 关闭游标
cursor.close()
# 提交更改
conn.commit()