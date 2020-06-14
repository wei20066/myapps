#coding:UTF-8
import datetime
import string
import xlrd
import socket
import logging
import datetime
import pymysql
import time
import threading

def get_data():
    '''
    读取txt文件中的数据
    '''
    dat=[]
    file=open('data.txt','r')
    for line in file.readlines():
        print(line)
        dat.append(line.strip())
			
#get_data()
def get_date():
	return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

def read_xls_file():
	'''
	读取Exl文件中的数据
	
	book = xlrd.open_workbook('3.xlsx')
#for sheet in book.sheets():
#    print(sheet.name)

sheet = book.sheet_by_name('3')
for i in range(sheet.nrows):
	devid=str(sheet.row_values(i)[1]).split(".")[0]
	head="TPJ{0}E0B01".format(devid)
	for j in range(sheet.nrows):
		cd=str(sheet.row_values(j)[2]).split(".")[0].zfill(10)
		cardid.append(head+cd+"DA")
for item in cardid:
	print(item)
	'''
	cardid=[]
	book = xlrd.open_workbook('3.xlsx')
	#for sheet in book.sheets():
	#    print(sheet.name)
	head="TPJ12345000E0B01"
	sheet = book.sheet_by_name('3')
	for i in range(sheet.nrows):
		cd=str(sheet.row_values(i)[2]).split(".")[0].zfill(10)
		cardid.append(head+cd+"DA")
	for item in cardid:
		print(item)
	
def sum_crc():	
	'''
	求校验和
	'''
	msg="0B013583713436"
	#TPJ12345000E0B013583713436DE
	str1=bytes(msg, encoding="utf8")
	num=int()
	for item in str1:
		num+=int(item)
	return hex(num)[3:5].upper()

def hex_to_dec():
	'''
	十六进制卡号转十进制
	'''
	str4="D5EEC3CC"
	print(int('0x'+str4,16))

def parse_msg():
	'''
	解析报文
	'''
	msg='TPJ18621                 018A080AD5EEC3CC            0001010222061000000D5EEC3CC            0001010227422000000D5E8772C            0001010227442000000D5E8772C            2003252041442000000D5F019EC            2003260950052000000D606986C            2003260950052000000D606982C            2003260950052000000D5E9097C            2003260950052000000D5EECA0C            2003260950052000000D5F0A35C            20032609500520000006D'
	print("通讯流水号:"+msg[3:7]+" 设备号："+ str(int(msg[7:25])) + " 功能号:" +msg[29:31]+ " 记录总条数:" + str(int('0x'+msg[31:33],16)))
	for i in range(int('0x'+msg[31:33],16)):
		recod=msg[33+i*39:33+(i+1)*39]
		cardid=int('0x'+recod[0:8],16)
		IOdate=recod[20:32]
		IOstatus="进" if recod[32:33]=="1" else "出"
		print("卡号："+str(cardid)+" 进出时间:"+IOdate[0:2]+"-"+IOdate[2:4]+"-"+IOdate[4:6]+" "+IOdate[6:8]+":"+IOdate[8:10]+":"+IOdate[10:12] +" 进出状态：" +IOstatus)
		
class A: 
	def x(self):
		print('run A.x')
		super().x()
		print(self)

class B:
	def x(self):
		print('run B.x')
		print(self)
		
class C(A,B):
	def x(self):
		print('run C.x')
		super().x()
		print(self)



def get_in_out_data(cardid):
	db = pymysql.connect("localhost","root","123456","Demo")
	cursor = db.cursor()
	swip_time=''
	device_id=''
	sql1 = "SELECT * FROM CARD_DATA WHERE CARD_ID = '%s' order by swip_time desc" % (cardid)
	sql2 =""
	cursor.execute(sql1)
	results = cursor.fetchall()
	for row in results:
		device_id =row[1]
		swip_time=row[3]
		print(device_id)
		print(swip_time)
	db.close()
		
get_in_out_data("3583454268")

print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
a = '2017-10-18 22:17:46'
b = '2017-10-19 22:17:40'
print (a > b)
#curTime=time.strftime("%Y-%M-%D",time.localtime())
#print(time.strftime("%b %d %Y %H:%M:%S", time.gmtime()))
from datetime import datetime
print(datetime(year=2015, month=7, day=4))
from dateutil import parser
date = parser.parse("4th of July, 2015")
print(date)

#import numpy as np
#date = np.array('2015-07-04', dtype=np.datetime64)
#print(date)
#np.datetime64('2015-07-04')
import datetime
d1 = datetime.datetime.strptime('2015-03-05 17:41:20', '%Y-%m-%d %H:%M:%S')
d2 = datetime.datetime.strptime('2015-03-05 17:41:30', '%Y-%m-%d %H:%M:%S')
print(d1)
delta = d1 - d2
print(delta.seconds)

now_time = str(time.time())
print(now_time.split('.')[0])


def socket_udp_server():
	s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#SOCK_DGRAM指类型是UDP
	host=''#监听指定的ip,host=''即监听所有的ip
	port=8080
    #绑定端口
	s.bind((host,port))	
	while True:
		data,addr=s.recvfrom(1024)
		print(data)
		if data: 
			sdt="JTP"+data[3:8].decode('ascii')+"00040BOKBD"
			print(sdt)
			s.sendto(sdt.encode('utf-8'),addr)
		else:
			continue

def main():
	p = threading.Thread(target=socket_udp_server, )
	p.start()

if __name__ == '__main__':
    #parse_msg()
	#print(sum_crc())
	#read_xls_file()
	#print(get_date())
	#get_data()
	C().x()