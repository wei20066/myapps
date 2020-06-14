#coding:UTF-8

import time
import socket
import random
from locust import Locust, TaskSet, events, task

class UdpSocketClient(socket.socket):
    # locust tcp client
    # author: Max.Bai@2017
    def __init__(self, af_inet, socket_type, ADDR):
        super(UdpSocketClient, self).__init__(af_inet, socket_type)
        self.ADDR = ADDR


    def send(self, msg):
        start_time = time.time()
        try:
            self.sendto(msg, self.ADDR)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="tcpsocket", name="send", response_time=total_time, exception=e, response_length=11)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="tcpsocket", name="send", response_time=total_time,
                                        response_length=0)

    def recv(self, bufsize):
        recv_data = ''
        start_time = time.time()
        try:
            recv_data = self.recvfrom(bufsize)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="tcpsocket", name="recv", response_time=total_time, exception=e, response_length=11)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="tcpsocket", name="recv", response_time=total_time,
                                        response_length=0)
        return recv_data

class UdpSocketLocust(Locust):
    """
    This is the abstract Locust class which should be subclassed. It provides an TCP socket client
    that can be used to make TCP socket requests that will be tracked in Locust's statistics.
    author: Max.bai@2017
    """
    def __init__(self, *args, **kwargs):
        super(UdpSocketLocust, self).__init__(*args, **kwargs)        
        self.host = "192.168.1.6"  
        ADDR = (self.host, self.port)        
        print('ADDR==',ADDR)
        self.client = UdpSocketClient(socket.AF_INET, socket.SOCK_DGRAM, ADDR)


class UdpTestUser(UdpSocketLocust):
    host = "192.168.1.6"    #连接的TCP服务的IP
    port = 8080      #连接的TCP服务的端口
    min_wait = 10
    max_wait = 100
    class task_set(TaskSet):
        data=[]
        def on_start(self):           
            file=open('data.txt','r')
            for line in file.readlines():
                self.data.append(line.strip())		

        @task
        def send_data1(self):
            #for item in self.data:
                #print(item)
            r=random.randint(0,581)
            print(self.data[r])
            self.client.send(bytearray(self.data[r], 'utf-8'))		#发送的数据
            rdata = self.client.recv(1024)
            print(rdata)



if __name__ == "__main__":
    user = UdpTestUser()
    user.run()
