#coding:utf-8
import Queue
from time import sleep,ctime
#from multiprocessing import Queue
from multiprocessing import Process


def pro1(q):
    while True:
        val=q.get(True)
        print '>>>>in por1:',val

def pro2(q):
    while True:
        val=q.get(True)
        print 'in por2:',val

#如果頭文件是import Queue
q=Queue.Queue()

#如果頭文件是from multiprocessing import Queue ，那執行
#q=Queue()

for i in range(20):
    q.put(i)
print 'start : ',ctime()
p1=Process(target=pro1,args=(q,))
p2=Process(target=pro2,args=(q,))
p1.start()
p2.start()

sleep(20)
print 'end : ',ctime()
pr.terminate()