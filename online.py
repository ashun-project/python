import datetime
import time
# def getYesterday(): 
#     today=datetime.date.today() 
#     tomr = today + datetime.timedelta(days=1)
    # oneday=datetime.timedelta(days=1) 
    # yesterday=today+oneday  
    # future = datetime.strptime(yesterday + ' 3:00:00', '%Y-%m-%d %H:%M:%S')
    # now = datetime.now()
    # sec = future - now
    # print(sec.seconds)
    # return sec.seconds
# print(getYesterday())
# today=datetime.date.today() 
# tomr = today + datetime.timedelta(days=1).now()
# y,m,d = str(tomr).split('-')

# sec = datetime.datetime(int(y),int(m),int(d),6,0,0)
# a = tomr.datetime.now()
# print(tomr)

# print(tomr, y,m,d, sec)



# from datetime import datetime
# #构造一个将来的时间
# future = datetime.strptime('2016-12-31 8:13:01','%Y-%m-%d %H:%M:%S')
# #当前时间
# now = datetime.now()
# #求时间差
# delta = future - now
# hour = delta.seconds/60/60
# minute = (delta.seconds - hour*60*60)/60
# seconds = delta.seconds - hour*60*60 - minute*60
# print delta.days, hour, minute, seconds
tom = datetime.date.today() + datetime.timedelta(days=1)
twelve = datetime.time(3,0,0)
tomTwelve = datetime.datetime.combine(tom, twelve)
tomTwelveSec = time.mktime(time.strptime(str(tomTwelve), '%Y-%m-%d %H:%M:%S'))
currentT = time.time()

print(tom, twelve, tomTwelve, tomTwelveSec,currentT,  int(tomTwelveSec - currentT))
