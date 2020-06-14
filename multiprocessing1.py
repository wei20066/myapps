#encoding:utf-8
import multiprocessing

def proc1(pipe):
    pipe.send("hello")
    print ("proc 1 : ",pipe.recv())

def proc2(pipe):
    print ("proc 2 : ",pipe.recv())
    pipe.send("hello ,too")
if __name__ == '__main__':
	#创建一个管道　这个管道是双向的
	pipe=multiprocessing.Pipe()
	#pipe[0]　表示管道的一端，pipe[1] 表示管道的另外一端
	#对pip的某一端调用send方法来传送对象，在另外一端使用recv来接收
	p1=multiprocessing.Process(target=proc1,args=(pipe[0],))
	p2=multiprocessing.Process(target=proc2,args=(pipe[1],))
	p1.start()
	p2.start()

	p1.join()
	p1.join()