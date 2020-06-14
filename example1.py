#import Queue
from time import sleep,ctime
from multiprocessing import Process,Queue

def pro1(q):
    while True:
        val=q.get(True)
        print '>>>>in por1:',val

def pro2(q):
    while True:
        val=q.get(True)
        print 'in por2:',val

q=Queue()
for i in range(101):
    q.put(i)
print 'start : ',ctime()
p1=Process(target=pro1,args=(q,))
p2=Process(target=pro2,args=(q,))
p1.start()
p2.start()

sleep(20)
print 'end : ',ctime()
pr.terminate()