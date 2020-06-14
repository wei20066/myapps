from time import sleep,ctime
from multiprocessing import Process

i=100
def proc1():
    global i
    count=1
    while True:
        print ('proc1 >>',i)
        i=i+2
        sleep(1)
        if count==5:
            break
        count=count+1

def proc2():
    global i
    count=1
    while True:
        print ('proc2 >>>>>>>>',i)
        i=i-3
        sleep(1)
        if count==5:
            break
        count=count+1
if __name__ == '__main__':
	print ("start")
	p1=Process(target=proc1)
	p2=Process(target=proc2)
	p1.start()
	p2.start()
	p1.join()
	p2.join()
	print ("end")