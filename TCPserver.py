#coding:UTF-8
import socket
import datetime

address=('192.168.0.2',2122)
server_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_sock.bind(address)
server_sock.listen(5)
new_socket,client_addr=server_sock.accept()
print('got connected from',client_addr)
while True:
    data=new_socket.recv(512)
    if data:
        if data[-4:-2].decode('ascii')=="0C":
            now=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            sdt="JTP"+data[3:15].decode('ascii')+"00100C"+now+"73"
            print(sdt)
            new_socket.send(bytearray(sdt, 'utf-8'))
        if data[-6:-4].decode('ascii')=="90":
            now=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            sdt="JTP"+data[3:15].decode('ascii')+"000509000A03"
            print(sdt)
            new_socket.send(bytearray(sdt, 'utf-8'))
        else:
            print(data)
            print("通讯流水号:"+msg[3:7]+" 设备号："+ str(int(msg[7:25])) + " 功能号:" +msg[29:31]+ " 记录总条数:" + str(int('0x'+msg[31:33],16))) 
            for i in range(int('0x'+data[31:33],16)):
                recod=data[33+i*39:33+(i+1)*39]
                cardid=int('0x'+recod[0:8],16)
                IOdate=recod[20:32]
                IOstatus="进" if recod[32:33]=="1" else "出"
                print("卡号："+str(cardid)+" 进出时间:"+IOdate[0:2]+"-"+IOdate[2:4]+"-"+IOdate[4:6]+" "+IOdate[6:8]+":"+IOdate[8:10]+":"+IOdate[10:12] +" 进出状态：" +IOstatus)
            sdt="JTP"+data[3:15].decode('ascii')+"000408OKBD"
            print(sdt)
            new_socket.send(bytearray(sdt, 'utf-8'))
    else:
        continue
    
new_socket.close()
