#coding:UTF-8
import socket
import logging
import queue
import datetime
import pymysql
import threading
q = queue.Queue()


def get_card_id(de_cardid):    
	str_hex=str(hex(de_cardid))
	if(len(str_hex)==8):
		str_hex=str_hex[0:2]+'00'+str_hex[2:8]
	if(len(str_hex)==9):
		str_hex=str_hex[0:2]+'0'+str_hex[2:9]
	order_str_hex=str_hex[8:10]+str_hex[6:8]+str_hex[4:6]+str_hex[2:4]
	cardid=int(order_str_hex,16)
	return cardid
		

def get_dec_card_id(dat):
	#return int(dat[16:26])
	return str(int(dat[16:26]))
	
def socket_udp_server():
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
	s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	host='192.168.0.2'
	port=8080
	s.bind((host,port))	
	while True:
		ls=[]
		data,addr=s.recvfrom(1024)
		ls.append(data)
		#now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
		now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		ls.append(now)
		q.put(ls)
		logger.info(ls[0])
		sdt="JTP"+data[3:8].decode('ascii')+"00040BOKBD"		
		s.sendto(sdt.encode('utf-8'),addr)

def save_data_to_db():
	db = pymysql.connect("localhost","root","123456","Demo")
	cursor = db.cursor()
	
	while True:
	   item = q.get()
	   if item is None:continue
	   print(item)
	   devid=item[0][3:8]
	   card_id=get_dec_card_id(item[0])
	   #card_id=get_card_id(dec_num)
	   swip_time=item[1][:23]
	   sql1 = "SELECT SWIP_TIME FROM CARD_DATA WHERE CARD_ID = '%s' and DEVICE_ID='%s' and STATUS='%s'" % (card_id,devid,'Y')
	   sql2 = "INSERT INTO CARD_DATA(DEVICE_ID, CARD_ID, SWIP_TIME, STATUS) VALUES ('%s', '%s', '%s','%s')" % (devid, card_id, swip_time,'Y')
	   sql3="DELETE FROM CARD_DATA WHERE CARD_ID = '%s' and DEVICE_ID !='%s'" % (card_id,devid)
	   sql4 = "SELECT SWIP_TIME DEVICE_ID FROM CARD_DATA WHERE CARD_ID = '%s' and DEVICE_ID !='%s'" % (card_id,devid)
	   sql5 ="update CARD_DATA set STATUS='%s' where CARD_ID = '%s' and DEVICE_ID='%s'" % ('N',card_id,devid)
	   try:
            cursor.execute(sql1)
            if(cursor.rowcount==0):
                cursor.execute(sql2)
                db.commit()
            if(cursor.rowcount>0):
                results = cursor.fetchall()
                for row in results:
                    swip_time1=row[0]
                d1 = datetime.datetime.strptime(str(swip_time1), '%Y-%m-%d %H:%M:%S')
                d2 = datetime.datetime.strptime(str(swip_time), '%Y-%m-%d %H:%M:%S')
                print(d2)
                delta = d2- d1
                print(delta.seconds)
                if(30 < delta.seconds):
                    cursor.execute(sql5)
                    cursor.execute(sql2)
	   except:
            db.rollback()
	   q.task_done()

def main():
	p = threading.Thread(target=socket_udp_server, )
	c = threading.Thread(target=save_data_to_db, )
	p.start()
	c.start()
	
main()