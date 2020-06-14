#coding:UTF-8
import socket
import logging

def create_socket(ipaddress,port):
	host=str(ipaddress)
	prot=int(port)
	sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	sock.bind((host,port))
	return sock
	
def set_param( sock, param_value, tupip ):
	#s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#SOCK_DGRAM指类型是UDP
	#host='192.168.0.2'#监听指定的ip,host=''即监听所有的ip
	#port=8080
    #绑定端口
	#s.bind((host,port))
	s=sock
	comannd=param_value
	ipstr=tupip
	while True:
		data,addr=s.recvfrom(1024)
		if(cmp(ipstr,addr)==0):		
			s.sendto(param_value,addr)
			data,addr=s.recvfrom(1024)
			if(cmp(ipstr,addr)==0 and str(data)=="OK"):
				s.sendto('AT+&W',addr)
				data,addr=s.recvfrom(1024)
			if(cmp(ipstr,addr)==0 and str(data)=="Write OK"):
				print("设置成功！！".decode('utf-8').encode('gbk'))
		exit(0)

def reset():
	set_reset="AT+&T"

def is_positive_integer(z):
    try:
        z_handle = int(z)
        if isinstance(z_handle,int) and z_handle >= 0: 
            return True 
    except:
        return False	
		
def main():
	set_interval="AT+DT=200"
	set_RSSI="AT+TR=127"
	set_DEVID="AT+ID=12340"
	set_GW="AT+GW=192.168.0.1"
	get_info="AT+&R"
	set_server_ip="AT+IP=192.168.0.2,8080"
	set_local_ip="AT+LIP=192.168.0.254,8080"
	ipaddress=('192.168.0.254',8080)
	sock=create_socket("192.168.0.2",8080)
	while True:
		print("*****************************************************")
		print("1.设置设备编号".decode('utf-8').encode('gbk'))
		print("2.设置RSSI参数值".decode('utf-8').encode('gbk'))
		print("3.设置服务器IP地址".decode('utf-8').encode('gbk'))
		print("4.设置本机IP地址".decode('utf-8').encode('gbk'))
		print("5.设置缓存时间间隔".decode('utf-8').encode('gbk'))
		print("6.设置本机网关".decode('utf-8').encode('gbk'))
		print("7.重启设备".decode('utf-8').encode('gbk'))
		print("8.输入q键退出".decode('utf-8').encode('gbk'))
		print("*****************************************************")
		print("请选择：".decode('utf-8').encode('gbk'))
		num=raw_input("input:")
		if(num=='1'):
			deviceid=''
			while True:
				print("1、请输入机号".decode('utf-8').encode('gbk'))
				print("2、返回上级菜单".decode('utf-8').encode('gbk'))
				num=raw_input("input:")
				if(num=='1'):
					devid=raw_input("input(1~65535):")
					if(is_positive_integer(devid) and int(devid)<=65535 and int(devid)>0 ):
						deviceid=devid
						strcommad="AT+ID="+deviceid
						set_param(sock,strcommad,ipaddress )
						break
				else:
					continue				
			break
		elif(num=='2'):
			set_param(sock, set_RSSI,ipaddress )
			break
		elif(num=='3'):
			set_param(sock, set_server_ip,ipaddress )
			break
		elif(num=='4'):
			set_param(sock, set_local_ip,ipaddress )
			break
		elif(num=='5'):
			set_param(sock, set_interval,ipaddress )
			break
		elif(num=='6'):
			set_param(sock, set_GW,ipaddress )
			break
		elif(num=='7'):
			set_param(sock, set_interval,ipaddress)
			break
		elif(num is 'q'):
			break
		else:
			continue
		
main()
