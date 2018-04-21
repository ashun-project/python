import os
import shutil
import time
path = "E:\\python\\nothing\\"
replacePath = "E:\\python\\list\\"
bb = int(time.time())
aa = str(bb)
print(aa, bb)
alllist = os.listdir(path)
for i in alllist:
    aa,bb = i.split(".")
    os.rename(path+'\\'+i, path+'\\'+'88.'+bb)
    oldname = path+'\\'+ '88.' + bb
    shutil.copyfile(oldname,replacePath+'\\88.'+bb)
    os.remove(path+'\\'+'88.'+bb)

    # if 'actor_hud' in aa.lower():
    #     oldname = u"D:\\Program Files\\Sublime Text 3\\image\\localres\\"+aa+"."+bb
    #     newname = u"D:\\Program Files\\Sublime Text 3\\image\\replace\\"+aa+"."+bb
    #     shutil.copyfile(oldname,newname)
    
