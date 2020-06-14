#coding:UTF-8
import socket
import logging

def get_card_id(de_cardid):    
	str_hex=str(hex(de_cardid))
	if(len(str_hex)==8):
		str_hex=str_hex[0:2]+'00'+str_hex[2:8]
	if(len(str_hex)==9):
		str_hex=str_hex[0:2]+'0'+str_hex[2:9]
	order_str_hex=str_hex[8:10]+str_hex[6:8]+str_hex[4:6]+str_hex[2:4]
	cardid=int(order_str_hex,16)
	return cardid
	
def get_data():
    #dat=[]
	#for line in file.readlines():
        #print(line)
        #dat.append(line.strip())
	card_sets=set()
	file=open('data.txt','r')
	for line in file.readlines():
		card_sets.add(str(line.strip()))
	return card_sets
		
def logger_init():
	logger = logging.getLogger("mylog")
	logger.setLevel(level=logging.DEBUG)
	handler = logging.FileHandler("log.txt")
	handler.setLevel(logging.INFO) 
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	handler.setFormatter(formatter)
	console = logging.StreamHandler()
	console.setLevel(logging.WARNING)
	logger.addHandler(handler)
	logger.addHandler(console)
	#logger.debug("show debug")
	#logger.warning("show warning")
	return logger

def socket_udp_server(sets,logger):
	s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#SOCK_DGRAM指类型是UDP
	host='192.168.1.5'#监听指定的ip,host=''即监听所有的ip
	port=8080
    #绑定端口
	s.bind((host,port))	
	number=0
	while True:
		data,addr=s.recvfrom(1024)
		cardid=int(data[16:26])
		#cardid=get_card_id(dat)
		#print(cardid)
		if str(cardid) in sets:
			number+=1
			print(number)
			print(cardid)
		sdt="JTP"+data[3:8].decode('ascii')+"00040BOKBD"
		logger.info(cardid)
		s.sendto(sdt.encode('utf-8'),addr)

def main():
	sets=get_data()	
	logger=logger_init()
	socket_udp_server(sets,logger)

main()