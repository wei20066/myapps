#coding:UTF-8
import socket
import threading
import time
import xlrd
import random

def send_thread(count):
	cardid=[]
	book = xlrd.open_workbook('3.xlsx')
	head="TPJ12345000E0B01"
	sheet = book.sheet_by_name('3')
	for i in range(sheet.nrows):
		cd=str(sheet.row_values(i)[2]).split(".")[0].zfill(10)
		cardid.append(head+cd+"DA")
	send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   
	for j in range(count):
		r=random.randint(0,581)
		print(cardid[r])
		time.sleep(2)
		send_socket.sendto(cardid[r].encode(), ('192.168.1.2', 8080))
	send_socket.close()
    
def recv_thread():
	recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	host=''#监听指定的ip,host=''即监听所有的ip
	port=8000
	#绑定端口
	recv_socket.bind((host,port))
	while True:
		time.sleep(2)
		recv_data = recv_socket.recvfrom(1024)
		if recv_data:
			print(recv_data)
			break
	recv_socket.close()

def main1(num,count):
	recv=threading.Thread(target=recv_thread, args=())
	recv.start()
	for i in range(num):
		print("thread"+str(i))
		client_thread = threading.Thread(target=send_thread, args=(count,))
		client_thread.start()
  
def socket_udp_server():
	s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#SOCK_DGRAM指类型是UDP
	host=''#监听指定的ip,host=''即监听所有的ip
	port=8080
    #绑定端口
	s.bind((host,port)) 
	while True:
		data,addr=s.recvfrom(1024)
		if data: 
			sdt="JTP"+data[3:8].decode('ascii')+"00040BOKBD"
			s.sendto(sdt.encode('utf-8'),(addr[0],8000))
		else:
			continue
			
def main():
	p = threading.Thread(target=socket_udp_server, )
	p.start()
 
if __name__=='__main__':
	main()