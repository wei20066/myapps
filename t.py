#coding:UTF-8
import datetime
import string
import binascii

def hanzi_strtohex(strhanzi):
	st1=strhanzi.encode('gbk')
def hanzi_hextostr(strhex):
	return 'Ok'
	
	



if __name__ == "__main__":
	s='B0A2B7B2CCE1C2F2'.lower()
	str1=''
	if len(s)%2==0:
		for i in range(int(len(s)/2)):
			str1=str1+'\\x'+s[i*2:i*2+2]
	print(str1)
	print(str2.decode('gbk'))
	#print(str1.decode('gbk'))
	print(s.encode())
	
	
	
=============================
st="TPJ022F53040002          00020C73"
print(st[-4:-2])
now=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
print(now)

'''
求校验和

#st1="TPJ12345000E0B013583713436DE"
st1="TPJ1234500140B0135837492440917281F"
str2=bytes(st1[12:32], encoding="utf8")
print(str2)
mun=int()
for item in str2:
   print(item)
   mun=mun+int(item)
str3=hex(mun)[3:5].upper()
print(str3)
'''
'''
十六进制卡号转十进制
'''
str4="D5EEC3CC"
print(int('0x'+str4,16))


'''
解析报文

msg='TPJ18621                 018A080AD5EEC3CC            0001010222061000000D5EEC3CC            0001010227422000000D5E8772C            0001010227442000000D5E8772C            2003252041442000000D5F019EC            2003260950052000000D606986C            2003260950052000000D606982C            2003260950052000000D5E9097C            2003260950052000000D5EECA0C            2003260950052000000D5F0A35C            20032609500520000006D'
print("通讯流水号:"+msg[3:7]+" 设备号："+ str(int(msg[7:25])) + " 功能号:" +msg[29:31]+ " 记录总条数:" + str(int('0x'+msg[31:33],16)))
for i in range(int('0x'+msg[31:33],16)):
    recod=msg[33+i*39:33+(i+1)*39]
    cardid=int('0x'+recod[0:8],16)
    IOdate=recod[20:32]
    IOstatus="进" if recod[32:33]=="1" else "出"
    print("卡号："+str(cardid)+" 进出时间:"+IOdate[0:2]+"-"+IOdate[2:4]+"-"+IOdate[4:6]+" "+IOdate[6:8]+":"+IOdate[8:10]+":"+IOdate[10:12] +" 进出状态：" +IOstatus)
'''
'''
python 三目运算
'''

a='1'
iostatus="进" if a=='1' else "出"
print(iostatus)
'''
字符串前面补0
'''
n = "123"
s = n.zfill(5)
print(s)

n = '-123'
s = n.zfill(5)
print(s)

n = 123
s = '%05d' % n
print(s)

def bytesToString(bs):
    return bytes.decode(bs,encoding='utf8')

def stringTobytes(str):
    return bytes(str,encoding='utf8')

def hexStringTobytes(str):
    str = str.replace(" ", "")
    return bytes.fromhex(str)
    # return a2b_hex(str)
	
def bytesToHexString(bs):
    # hex_str = ''
    # for item in bs:
    #     hex_str += str(hex(item))[2:].zfill(2).upper() + " "
    # return hex_str
    return ''.join(['%02X ' % b for b in bs])
	
b = b"Hello, world!"  # bytes object  
s = "Hello, world!"   # str object 

hex(16)     # 10进制转16进制
oct(8)      # 10进制转8进制
bin(8)      # 10进制转2进制

int('10')       # 字符串转换成10进制整数
int('10',16)    # 字符串转换成16进制整数
int('0x10',16)  # 字符串转换成16进制整数
int('10',8)     # 字符串转换成8进制整数
int('010',8)    # 字符串转换成8进制整数
int('10',2)     # 字符串转换成2进制整数

print('str --> bytes')
print(bytes(s, encoding="utf8"))    
print(str.encode(s))   # 默认 encoding="utf-8"
print(s.encode())      # 默认 encoding="utf-8"

print('\nbytes --> str')
print(str(b, encoding="utf-8"))   
print(bytes.decode(b))  # 默认 encoding="utf-8"
print(b.decode())       # 默认 encoding="utf-8"


import os,sys

# global definition
# base = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, C, D, E, F]
base = [str(x) for x in range(10)] + [ chr(x) for x in range(ord('A'),ord('A')+6)]

# bin2dec
# 二进制 to 十进制: int(str,n=10) 
def bin2dec(string_num):
    return str(int(string_num, 2))

# hex2dec
# 十六进制 to 十进制
def hex2dec(string_num):
    return str(int(string_num.upper(), 16))

data = b'data'
output = binascii.hexlify(data)

# dec2bin
# 十进制 to 二进制: bin() 
def dec2bin(string_num):
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num,rem = divmod(num, 2)
        mid.append(base[rem])

    return ''.join([str(x) for x in mid[::-1]])
	
import sys

#choose = sys.argv[1]
#data = sys.argv[2]

def hex2char():
    output = data.decode('hex')
    print(output)
  
def char2hex():
    output = data.encode('hex')
    print(output)
	
def hex2char(data):
#    binascii.a2b_hex(hexstr) 
    output = binascii.unhexlify(data)
    print(output)

def char2hex(data):
    data = b'data'
#    binascii.b2a_hex(data) 
    output = binascii.hexlify(data)
    print(output)

print("Usage:  <filename> <hex2char or char2hex> <your data>")

if len(sys.argv) == 3:
    if choose.lower() == 'hex2char':
        hex2char()
       
    if choose.lower() == 'char2hex':
        char2hex()
    
    if choose.lower()!='hex2char' and choose.lower()!='char2hex':
        print("Wrong param,try again")
else:
    print("Wrong number of params,check your input\n")

#this script has passed the test

#ret = binascii.b2a_hex(sign)

def HexToByte( hexStr ):
    return bytes.fromhex(hexStr)

def ByteToHex( bins ):
    return ''.join( [ "%02X" % x for x in bins ] ).strip()
	
my_str = '     hello WORLD'
print(my_str.lstrip())
	
binascii.b2a_hex(u"你好啊".encode("utf8"))
binascii.b2a_hex(u"你好啊".encode("gbk"))
binascii.a2b_hex("e4bda0e5a5bde5958a")
binascii.a2b_hex("e4bda0e5a5bde5958a").decode("utf8")
binascii.b2a_hex(u"你好啊121A号".encode("gbk"))
#u"你好啊121A号".encode("gbk").encode('hex')
#'c4e3bac3b0a131323141bac5'.decode('hex')
#55BB4200 00001E306C2E000429049000ED020000C0A8006CFFFFFF00C0A8000100C0A80002901F00C0A800028E4EFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF1A 55EE
#1E306C2E000429307500200330144440030000000000323032303033313031313230010101C0A8006C
#55BB420000001E306C2E000429049000EF020000C0A8006CFFFFFF00C0A8000100C0A80002901F00C0A800028E4EFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF1C55EE
info="55BB420000001E306C2E000429A49000E80000012B00000001200430B0A2B7B2CCE1C2F21234567800000001000000000000000002FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD555EE"
print(int(info[6:8]+info[4:6],16))
#print(str(hex(66))[2:4])

def dec2hex(string_num):
	num = int(string_num)
	mid = []
	while True:
		if num == 0: break
		num,rem = divmod(num, 16)
		mid.append(base[rem])
	return ''.join([str(x) for x in mid[::-1]])
 
print(dec2hex('66'))

import re 
  
def Find(string): 
    # findall() 查找匹配正则表达式的字符串
    url = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', string)
    return url 
#string = 'Runoob 的网页地址为：https://www.runoob.com，Google 的网页地址为：https://www.google.com'
#print("Urls: ", Find(string))

string2="""POST http://192.168.0.2:8088/api/services/hwd/QPlus/heartBeatApi HTTP/1.1
Accept: */*
Cache-Control: no-cache
Content-Type: application/json;charset=UTF-8
User-Agent: Dalvik/2.1.0 (STM32; NO SYSTEM)
Connection: Keep-Alive
Accept-Encoding: gzip, deflate
Host:192.168.0.2:8088
content-length: 122

{"content":"1E306C2E000329307500200422082108090000010000323032303034313830393136020101C0A8002A","access":"","instruct":""}
string = 'Runoob 的网页地址为：https://www.runoob.com，Google 的网页地址为：https://www.google.com'
"""
str1="""POST http://192.168.0.2:8080/api/services/hwd/QPlus/uploadingApi HTTP/1.1
Accept: */*
Cache-Control: no-cache
Content-Type: application/json;charset=UTF-8
User-Agent: Dalvik/2.1.0 (STM32; NO SYSTEM)
Connection: Keep-Alive
Accept-Encoding: gzip, deflate
Host:192.168.0.2:8080
content-length: 212

{"content":"55BB500000001E306C2E000329A3CCCC0000003075003B030000000000002004221037390314FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE255EE","access":"","instruct":""}POST http://192.168.0.2:8080/api/services/hwd/QPlus/statusDevApi HTTP/1.1
Accept: */*
Cache-Control: no-cache
Content-Type: application/json;charset=UTF-8
User-Agent: Dalvik/2.1.0 (STM32; NO SYSTEM)
Connection: Keep-Alive
Accept-Encoding: gzip, deflate
Host:192.168.0.2:8080
content-length: 124

{"content":"55BB240000001E306C2E000329A500000000002004221037390004000400AAFFFFFFFFFFFFFFFF2955EE","access":"","instruct":""}
"""
str2="""
POST http://192.168.0.2:8080/api/services/hwd/QPlus/statusDevApi HTTP/1.1
Accept: */*
Cache-Control: no-cache
Content-Type: application/json;charset=UTF-8
User-Agent: Dalvik/2.1.0 (STM32; NO SYSTEM)
Connection: Keep-Alive
Accept-Encoding: gzip, deflate
Host:192.168.0.2:8080
content-length: 124

{"content":"55BB240000001E306C2E000329A500000000002004221047130004000400AAFFFFFFFFFFFFFFFF1355EE","access":"","instruct":""}
"""
import json
#print(string2.split(' ')[1].split('/')[-1])
#print(len(str2))
#print('{'+str1.split('{')[1].split('}')[0]+'}')
#print('{'+str1.split('{')[2].split('}')[0]+'}')
res=json.loads('{'+str1.split('{')[1].split('}')[0]+'}')
print(res)

#str = "Line1-abcdef \nLine2-abc \nLine4-abcd";
#print (str.split( ))     # 以空格为分隔符，包含 \n
#print (str.split(' ', 1 )) # 以空格为分隔符，分隔成两个


	#s= b'\xe4\xb8\xad\xe5\x9b\xbd'
	s=b'B0A2B7B2CCE1C2F2'.lower()
	print(s)
	#print(s.decode('gbk'))
	s = u'xe6x97xa0xe5x90x8d' 
	s2 = s.encode('raw_unicode_escape')
	print(s2)
	s = '远程控制'
	a = s.encode('gbk')
	#print(a.decode('ascii'))
	print(a.decode('gbk'))
	s1=b'\xb0\xa2\xb7\xb2\xcc\xe1\xc2\xf2'
	print(s1.decode('gbk'))
	code = b'\xe8\xb1\x86\xe7\x93\xa3'
	print(code.decode())
	
#coding:UTF-8
import socket
import threading
import time
import xlrd

def subthread(count):
	cardid=[]
	book = xlrd.open_workbook('3.xlsx')
	head="TPJ12345000E0B01"
	sheet = book.sheet_by_name('3')
	for i in range(sheet.nrows):
		cd=str(sheet.row_values(i)[2]).split(".")[0].zfill(10)
		cardid.append(head+cd+"DA")
	udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	for j in range(count):
	
    #while True:
        # 从键盘获取数据(第二种方法)
        #send_data = input('请输入要发送的内容：')
		#print(str(j))
        # 如果输入的数据是exit,那么就退出程序
		#if send_data == 'exit':
            #break
			#bytearray(data, 'utf-8')
		udp_socket.sendto(cardid[j].encode(), ('192.168.2.14', 8080))
		time.sleep(0.001)
		while True:
			try:
				recv_data = udp_socket.recvfrom(1024)
				if recv_data:
					print(recv_data)
					break
				else:
					print("no data")
					continue
			except Exception as tp:
				continue
    #udp_socket.close()
def main(num,count):
	 for i in range(num):
		print("thread"+str(i))
		client_thread = threading.Thread(target=subthread, args=(count,))
		client_thread.start()
	

if __name__ == '__main__':
    main(2,1000)
