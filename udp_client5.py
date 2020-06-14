# -*- coding:utf-8 -*-

import time
import socket
import random
import queue
from locust import Locust, TaskSet, events, task

class UdpSocketClient(socket.socket):
    # locust tcp client
    # author: Max.Bai@2017
    def __init__(self, af_inet, socket_type, ADDR):
        super(UdpSocketClient, self).__init__(af_inet, socket_type)
        self.ADDR = ADDR


    def send(self, msg, device):
        start_time = time.time()
        self.device = device
        try:
            self.sendto(msg, self.ADDR)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="udpsocket", name="send", response_time=total_time, exception=e, response_length=11)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="udpsocket", name="send", response_time=total_time,
                                        response_length=0)

    def recv(self, bufsize):
        recv_data = ''
        start_time = time.time()
        try:
            recv_data = self.recvfrom(bufsize)
            total_time = int((time.time() - start_time) * 1000)
            if str(recv_data[0][3:8].decode('ascii')) != self.device:
                events.request_failure.fire(request_type="udpsocket", name="recv", response_time=total_time, exception=None, response_length=11)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="udpsocket", name="recv", response_time=total_time, exception=e, response_length=11)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="udpsocket", name="recv", response_time=total_time,
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
        self.host = "192.168.1.170"
        ADDR = (self.host, self.port)
        print('ADDR==',ADDR)
        self.client = UdpSocketClient(socket.AF_INET, socket.SOCK_DGRAM, ADDR)


class UdpTestUser(UdpSocketLocust):
    host = "192.168.1.170"            #连接的TCP服务的IP
    port = 8080                      #连接的TCP服务的端口
    min_wait = 100
    max_wait = 1000

    class task_set(TaskSet):
        def on_start(self):
            self.device_id = '00000'
            try:
                device_id = Devices_queue.get() # 获取队列里的数据
                Devices_queue.put_nowait(device_id)
            except queue.Empty:                 # 队列取空后，直接退出
                print("no device_id exist")
                exit(0)
            self.device_id = device_id 
            print('Device Init ID:{0}'.format(device_id))            
     
        def on_stop(self):
            print('Device exit ID:{0}'.format(self.device_id))

        @task
        def send_data(self):
            index =  random.randint(0,len(Cards)-1)
            card = Cards[index]
            data = "TPJ{0}000E0B01{1}DA".format(self.device_id, card)
            print("sent: {0}".format(data))
            self.client.send(bytearray(data, 'utf-8'), self.device_id)      #发送的数据
            data = self.client.recv(1024)
            print("received:{0}".format(data))

Devices_queue = queue.Queue()  # 设备队列

Devices = []
Cards = []

# 加载设备和卡号
def load_from_csv():
    import csv,sys
    print(sys.path[0])
    f_devices =open(sys.path[0]+'/devices.csv',mode='r')
    csv_reader=csv.reader(f_devices)
    for row in csv_reader:
        a =  [x for x in row if x != '']
        Devices.extend(a)
    print(Devices)
    f_devices.close()
    
    f_cards = open(sys.path[0]+'/cards.csv',mode='r')
    csv_reader=csv.reader(f_cards)
    for row in csv_reader:
        a =  [x for x in row if x != '']
        Cards.extend(a)
    print(Cards)
    f_cards.close()
    
    for x in Devices:
      Devices_queue.put_nowait(x)

load_from_csv()

if __name__ == "__main__":
    user = UdpTestUser()
    user.run()
