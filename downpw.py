#coding:UTF-8
import socket
import threading
import json
import datetime

def hextodec(strhex):
	if len(strhex)==8:
		return int('0x'+strhex[6:8]+strhex[4:6]+strhex[2:4]+strhex[0:2],16)
	else:
		return False 

def cardid_dectohex(strdec):
	str1=str(hex(int(strdec)))[2:].zfill(8)
	str2=str1[6:8]+str1[4:6]+str1[2:4]+str1[0:2]
	return str2.upper()

def gethttphead(req):
	GMT_FORMAT =  '%a, %d %b %Y %H:%M:%S GMT'
	dat=datetime.datetime.utcnow().strftime(GMT_FORMAT)
	response = "HTTP/1.1 200 OK\r\n"
	response +="Content-Type: text/plain;charset=UTF-8\r\n"
	response +="Content-Length:"+str(len(json.dumps(req)))+"\r\n"
	response +="date: " +dat+"\r\n"
	response += "\r\n"
	response += json.dumps(req)
	return response

def service_client(new_socket):
	"""为这个客户端返回数据"""

    # 1. 接收浏览器发送过来的请求 ，即http请求  
    # GET / HTTP/1.1
    # .....
	while True:
		request = new_socket.recv(1024)
		if not request: break
		bs = bytes.decode(request)
		try:
			path=bs.split(' ')[1].split('/')[-1]
		except IndexError:
			continue
		#res=json.loads(bs.split('\r\n\r\n', 1)[1])
		res=json.loads('{'+bs.split('{')[1].split('}')[0]+'}')		
		if('heartBeatApi'==path):
			print('心跳:'+res['content'])
			if(res['content'][18:20]=='00'): #判断是否为心跳包
				nowTime = datetime.datetime.now()
				strTime = nowTime.strftime("%y%m%d%H%M%S")
				content=res['content'][0:12]+res['content'][14:18]+'00'+strTime
				stat=res['content'][70:72]
				req=json.loads('{"access":"","content":"","instruct":""}')
				req['content']=content+stat
				req['access']='55BB420000001E306C2E000329A490004400000153CE300001200430B0A2B7B2CCE1C2F21234567800000001000000000000000003FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF5755EE'				
				new_socket.send(gethttphead(req).encode("utf-8"))
		if('accessApi'==path):
			if(res['access'][26:28]=='A4'): #判断是否为心跳包
				access=res['access'][0:4]+'14000000'+res['access'][12:30]+'000000000005855EE'
				print(access)
				req=json.loads('{"access":"","content":"","instruct":""}')
				req['access']=access
				new_socket.send(gethttphead(req).encode("utf-8"))
				
		

def main():
    """用来完成整体的控制"""
    # 1. 创建套接字
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 2. 绑定
    tcp_server_socket.bind(("", 8088))

    # 3. 变为监听套接字
    tcp_server_socket.listen(128)
    #old_addr=""
    while True:
        # 4. 等待新客户端的链接
        new_socket, client_addr = tcp_server_socket.accept()
        #if(client_addr[0]!=old_addr):
            #print(client_addr[0])
            #old_addr=client_addr[0]
        handle_client_thread = threading.Thread(target=service_client, args=(new_socket,))
        handle_client_thread.start()
				

        # 5. 为这个客户端服务
        #service_client(new_socket)
       
       

    # 关闭监听套接字
    tcp_server_socket.close()


if __name__ == "__main__":
    main()