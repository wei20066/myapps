#coding:UTF-8
import socket
import threading
import time
import xlrd
import random
def subthread(count):
	cardid=[]
	book = xlrd.open_workbook('3.xlsx')
	head="TPJ12345000E0B01"
	sheet = book.sheet_by_name('3')
	host="192.168.0.2"
	port= 8800
	for i in range(sheet.nrows):
		cd=str(sheet.row_values(i)[2]).split(".")[0].zfill(10)
		cardid.append(head+cd+"DA")
	udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	udp_socket.setblocking(False)
	udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	udp_socket.bind((host,port))
	for j in range(count):
	
    #while True:
        # 从键盘获取数据(第二种方法)
        #send_data = input('请输入要发送的内容：')
		#print(str(j))
        # 如果输入的数据是exit,那么就退出程序
		#if send_data == 'exit':
            #break
			#bytearray(data, 'utf-8')
		r=random.randint(0,581)
		udp_socket.sendto(cardid[r].encode(), ('192.168.2.14', 8080))
		print(cardid[r])
		time.sleep(1)
		'''
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
		'''		
    #udp_socket.close()
def main(num,count):
    for i in range(num):
        print("thread"+str(i))
        client_thread = threading.Thread(target=subthread, args=(count,))
        client_thread.start()
	

if __name__ == '__main__':
    main(4,10)
