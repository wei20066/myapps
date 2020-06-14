#coding:UTF-8
import socket
import datetime
import threading
		

def socket_udp_server():
	s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#SOCK_DGRAM指类型是UDP
	host='192.168.0.2'#监听指定的ip,host=''即监听所有的ip
	port=8080
    #绑定端口
	s.bind((host,port))	
	while True:
		data,addr=s.recvfrom(1024)
		if data:
			print(data)
			print("卡号："+data[16:26].decode('ascii')+"时间："+data[26:33].decode('ascii'))
			if data[-4:-2].decode('ascii')=="0C":
				now=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
				sdt="JTP"+data[3:8].decode('ascii')+"00100C"+now+"73"
				print(sdt)
				s.sendto(sdt.encode('utf-8'),addr)
			else:
				sdt="JTP"+data[3:8].decode('ascii')+"00040BOKBD"
				print(sdt)
				s.sendto(sdt.encode('utf-8'),addr)			
		else:
			continue

def main():
	p = threading.Thread(target=socket_udp_server, )
	p.start()
	
main()