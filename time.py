#coding:UTF-8
__author__ = 'Administrator'
import os,threading,time
import datetime
curTime=datetime.datetime.now().strftime("%Y-%m-%d")
#curTime=time.strftime("%Y-%M-%D",time.localtime())  #记录当前时间
execF=False
ncount=0

def execTask():
  #具体任务执行内容
  print("execTask executed!")

def timerTask():
  global execF
  global curTime
  global ncount
  if execF is False:
    execTask()#判断任务是否执行过，没有执行就执行
    execF=True
  else:#任务执行过，判断时间是否新的一天。如果是就执行任务
    #desTime=time.strftime("%Y-%M-%D",time.localtime())
    desTime=datetime.datetime.now().strftime("%Y-%m-%d")
    if desTime > curTime :
        execF = False #任务执行执行置值为
        curTime=desTime
  ncount = ncount+1
  timer = threading.Timer(10,timerTask)
  timer.start()
  print(ncount)

if __name__=="__main__":
  timer = threading.Timer(10,timerTask)
  timer.start()