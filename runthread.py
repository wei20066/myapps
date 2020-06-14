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
    for i in range(sheet.nrows):
        cd=str(sheet.row_values(i)[2]).split(".")[0].zfill(10)
        cardid.append(head+cd+"DA")
	
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for j in range(count):	
        r=random.randint(0,581)
        print(cardid[r])
        send_socket.sendto(cardid[r].encode(), ('192.168.1.2', 8080))
        while True:
            recv_data = send_socket.recvfrom(1024)
            if recv_data:
               print(recv_data)
               break
    send_socket.close()

def main(num,count):
    for i in range(num):
        print("thread"+str(i))
        client_thread = threading.Thread(target=subthread, args=(count,))
        client_thread.start()
if __name__ == '__main__':
    main(1,100)