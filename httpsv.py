#coding:UTF-8
import socket
import threading
import json
import datetime

def service_client(new_socket):
	"""为这个客户端返回数据"""

    # 1. 接收浏览器发送过来的请求 ，即http请求  
    # GET / HTTP/1.1
    # .....
	while True:
		request = new_socket.recv(1024)
		if not request: break
		res=json.loads('{'+request.split('{')[1])
		if(res['content']!=""):
			print(res['content'])
		# 2. 返回http格式的数据，给浏览器
		# 2.1 准备发送给浏览器的数据---header
		nowTime = datetime.datetime.now()
		strTime = nowTime.strftime("%y%m%d%H%M%S")
		#content='{"access":"","content":"1E306C2E000330750020030510461201","instruct":""}'
		req=json.loads('{"access":"","content":"","instruct":""}')
		req['content']='1E306C2E0003307500'+strTime+'01'
		GMT_FORMAT =  '%a, %d %b %Y %H:%M:%S GMT'
		dat=datetime.datetime.utcnow().strftime(GMT_FORMAT)
		response = "HTTP/1.1 200 OK\r\n"
		response +="Content-Type: text/plain;charset=UTF-8\r\n"
		response +="Content-Length:"+str(len(req))+"\r\n"
		response +="date: " +dat+"\r\n"
		response += "\r\n"
		# 2.2 准备发送给浏览器的数据---boy
		response += json.dumps(req, 0) 
		#print(response)
		new_socket.send(response.encode("utf-8"))
	
		# 关闭套接字
		#new_socket.close()
		

def main():
    """用来完成整体的控制"""
    # 1. 创建套接字
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 2. 绑定
    tcp_server_socket.bind(("", 8000))

    # 3. 变为监听套接字
    tcp_server_socket.listen(128)
    old_addr=""
    while True:
        # 4. 等待新客户端的链接
        new_socket, client_addr = tcp_server_socket.accept()
        if(client_addr[0]!=old_addr):
            print(client_addr[0])
            old_addr=client_addr[0]
            handle_client_thread = threading.Thread(target=service_client, args=(new_socket,))
            handle_client_thread.start()
				

        # 5. 为这个客户端服务
        #service_client(new_socket)
       
       

    # 关闭监听套接字
    tcp_server_socket.close()


if __name__ == "__main__":
    main()