# coding:utf-8
import serial
import serial.tools.list_ports
import binascii
import struct
import locale
import time

#key_word = [0xAA, 0x38, 0x08, 0x00, 0x01, 0xAD, 0x18, 0xB9, 0xAC, 0xE5, 0xC0, 0xBA, 0xBB]
#auth_word_sector1 = [0xAA, 0x34, 0x02, 0x00, 0x01, 0xE1, 0xBB]

class Com:
	def __init__(self,port,baudrate):
		self.port=port
		self.baudrate=baudrate
		self.opening=False
		self.com=None

	def open(self):
		if self.opening==False:
			self.com=serial.Serial(str(self.port),self.baudrate, timeout=60)
			self.opening=True
		
	def write(self,data):
		self.com.write(struct.pack("%dB" % len(data), *data))
    
	def read(self,count):
		return ''.join(['%02X' % b for b in self.com.read(count)])
		

class Reader(Com):	
	def __init__(self,port,baudrate):
		super(Reader,self).__init__(port,baudrate)
		
	def reader_beep(self,beep):
		if self.opening==False:
			self.open()
		self.write(beep)
		back_data = self.read(7)[6:10]
		if back_data == '0000':
			return True
		else:
			return False
		
	def reader_search(self,search):
		if self.opening==False:
			self.open()
		self.write(search)
		back_data = self.read(10)
		if back_data[8:12] == '0000':
			return False
		else:
			return back_data
	
	def reader_halt(self,halt):
		if self.opening==False:
			self.open()
		self.write(halt)
		back_data = self.read(7)[6:10]
		if back_data == '0000':
			return False
		else:
			return True
	
	def reader_load_key(self,key):
		if self.opening==False:
			self.open()
		self.write(key)
		back_data = self.read(7)[6:10]
		if back_data == '0000':
			#print("load_key success")
			return True
		else:
			print("load_key failed")
			return False
	
	def reader_auth_key(self,auth_key):
		if self.opening==False:
			self.open()
		self.write(auth_key)
		back_data = self.read(7)[6:10]
		if back_data == '0000':
			#print("auth success")
			return True
		else:
			print("auth failed")
			return False


class RFReader(Reader):
	success_beep = [0xAA, 0x30, 0x05, 0x05, 0xDC, 0x05, 0xDC, 0x01, 0xA2, 0xBB]
	failed_beep = [0xAA, 0x30, 0x05, 0x05, 0xDC, 0x05, 0xDC, 0x01, 0xA2, 0xBB]
	def __init__(self,port,baudrate):
		super(RFReader,self).__init__(port,baudrate)
		
	def read_block(self,sector,block):	
		if self.reader_auth_key(sector)==True:
			self.write(block)
			#data=self.read(22)
			data=self.read(22)[6:38]
			self.reader_beep(self.success_beep)
			return data
		else:
			self.reader_beep(self.failed_beep)
			return False

class CardReader(RFReader):
	search = [0xAA, 0x3B, 0x01, 0x00, 0xE6, 0xBB]
	halt = [0xAA, 0x35, 0x01, 0x00, 0xE0, 0xBB]
		
	def __init__(self,port,baudrate):
		super(CardReader,self).__init__(port,baudrate)
	
	def read_sector(self,key,tag):
		if tag=='baes_sector':
			sector = [0xAA, 0x34, 0x02, 0x01, 0x01, 0xE2, 0xBB]
			block = [0xAA, 0x36, 0x01, 0x04, 0xE5, 0xBB]
			arr=[]
			result=self.reader_search(self.search)
			if result==False:
				print("can't find card")
			else:
				arr.append(result[6:14])
				if self.reader_load_key(key)==True:		
					st1=self.read_block(sector,block)
					arr.append(st1)
					block[3]=0x05
					block[4]=0xE6
					st2=self.read_block(sector,block)
					arr.append(st2)
					block[3]=0x06
					block[4]=0xE7
					st3=self.read_block(sector,block)
					arr.append(st3)
					self.reader_halt(self.halt)
					return arr
		
		if tag=="XF_sector1":
			sector = [0xAA, 0x34, 0x02, 0x01, 0x04, 0xE5, 0xBB]
			block = [0xAA, 0x36, 0x01, 0x10, 0xF1, 0xBB]
			result=self.reader_search(self.search)
			if result==False:
				print("can't find card")
			else:
				if self.reader_load_key(key)==True:			
					arr=[]
					st1=self.read_block(sector,block)
					arr.append(st1)
					block[3]=0x11
					block[4]=0xF2
					st2=self.read_block(sector,block)
					arr.append(st2)
					block[3]=0x12
					block[4]=0xF3
					st3=self.read_block(sector,block)
					arr.append(st3)
					self.reader_halt(self.halt)
					return arr
					
		if tag=="XF_sector2":
			sector = [0xAA, 0x34, 0x02, 0x01, 0x05, 0xE6, 0xBB]
			block = [0xAA, 0x36, 0x01, 0x14, 0xF5, 0xBB]
			result=self.reader_search(self.search)
			if result==False:
				print("can't find card")
			else:
				if self.reader_load_key(key)==True:						
					block[3]=0x14
					block[4]=0xF5
					arr=[]
					st1=self.read_block(sector,block)
					arr.append(st1)
					block[3]=0x15
					block[4]=0xF6
					st2=self.read_block(sector,block)
					arr.append(st2)
					block[3]=0x16
					block[4]=0xF7
					st3=self.read_block(sector,block)
					arr.append(st3)
					self.reader_halt(self.halt)
					return arr
		
def cardID_WG34(data):
	cardid_WG34=data[6:8]+data[4:6]+data[2:4]+data[0:2]
	cardid_WG34=int("0x"+cardid_WG34,16)#4位物理卡号
	return str(cardid_WG34)

def cardID_WG26(data):
	cardid_WG26=data[4:6]+data[2:4]+data[0:2]
	cardid_WG26=int("0x"+ cardid_WG26,16)#3位物理卡号
	return str(cardid_WG26)

def cardID_WT26(data):
	cardID_WT26=data[4:6]+data[2:4]+data[0:2]
	cardID_WT26=int("0x"+ cardID_WT26,16)#3位物理卡号
	return str(cardID_WT26)
	
def valid_date(data):
	valid_date="20"+data[6:8]+"-"+data[8:10]+"-"+data[10:12]
	return valid_date
	
def emp_id(data):
	emp_id=data[14:]
	return emp_id
	
def emp_sex(data):
	if data[12:14]=='11':
		return "male"
	if data[12:14]=='10':
		return "female"
def emp_display_id(data):
	display_id=str(chr(int(data[16:18],16))+chr(int(data[18:20],16))+chr(int(data[20:22],16))+chr(int(data[22:24],16))+chr(int(data[24:26],16))+chr(int(data[26:28],16))+chr(int(data[28:30],16))+chr(int(data[30:32],16))).strip()
	return display_id

def emp_name(data):
	emp_name= gbk_incode_to_hanzi(data[0:16])
	return emp_name

def pay_password(data):
	pay_password=data[4:6]+data[2:4]+data[0:2]
	pay_password=int("0x"+pay_password,16)
	return str(pay_password)
	

def gbk_incode_to_hanzi(data):
    emp_name =""
    for i in range(0, len(data), 4):
        if data[i:i + 4] != '0000':
            hw = hex(int(str(int("0x" + data[i:i + 4], 16))[0:2]) + int("0xA0", 16))[2:4]
            lw = hex(int(str(int("0x" + data[i:i + 4], 16))[2:4]) + int("0xA0", 16))[2:4]# 汉字gbk内码转gbk编码
            emp_name = emp_name + hw + lw
            continue
        else:
            break
    return binascii.a2b_hex(emp_name).decode("GB2312")#gbk编码汉字
 
def cal_money(hex_vlue):
    value =hex_vlue[4:6]+hex_vlue[2:4]+hex_vlue[0:2]
    return locale.format("%.2f", int(value,16)/100, 1)
def cal_times(hex_vlue):
    value = hex_vlue[4:6] + hex_vlue[2:4] + hex_vlue[0:2]
    return str(int(value,16))
def cal_date(hex_vlue):
    value = hex_vlue[6:8] + hex_vlue[4:6] + hex_vlue[2:4] + hex_vlue[0:2]
    timeArray = time.localtime(int(value, 16))
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return str(otherStyleTime)

def valid_sum(str1):#远距离读头报文的校验和
	str2=bytes(str1, encoding="utf8")
	mun=int()
	for i in str2:
		mun=mun+int(i)
	return hex(mun)[-2:].upper()	
		
def hex_valid_sum(arry):
	sum=0;
	for i in range(0,len(arry)):
		sum=sum+arry[i]
	return int("0x"+hex(sum)[-2:].upper(),16)

class M1_Card():
	def __init__(self):
		self.cardid_WG34=""
		self.cardid_WG26=""
		self.cardid=""
		
if __name__ == '__main__':
	
	ser=CardReader('COM3',115200)
	key =  [0xAA, 0x38, 0x08, 0x01, 0x01, 0xDF, 0xA6, 0x40, 0xE3, 0x15, 0x49, 0xF2, 0xBB]
	base=ser.read_sector(key,"baes_sector")
	key[4]=0x04
	key[11]=0xF5
	XF1=ser.read_sector(key,"XF_sector1")
	key[4]=0x05
	key[11]=0xF6
	XF2=ser.read_sector(key,"XF_sector2")
	print(base)
	print("四字节卡号："+cardID_WG34(base[0])+" 三字节卡号："+cardID_WG26(base[0])+" 卡流水号："+cardID_WT26(base[1])+ " 卡有效期："+valid_date(base[1]))
	print(" 性别："+emp_sex(base[1])+" 身份证号："+emp_id(base[1])+" 工号： "+emp_display_id(base[2])+" 姓名："+emp_name(base[3]))
	print(XF1)
	print("支付密码: "+pay_password(XF1[0][12:16]))
	print("卡余额："+cal_money(XF1[0][16:22]))
	print("卡使用次数："+ cal_times(XF1[1][0:6]))
	print(XF2)