# coding:utf-8
import serial
import serial.tools.list_ports
import binascii
import struct
import locale
import time
start_byte =0xAA
end_byte=0xBB
beep_word = [0xAA, 0x30, 0x05, 0x05, 0xDC, 0x05, 0xDC, 0x01, 0xA2, 0xBB]
find_card = [0xAA, 0x3B, 0x01, 0x00, 0xE6, 0xBB]
halt_word = [0xAA, 0x35, 0x01, 0x00, 0xE0, 0xBB]
key_word = [0xAA, 0x38, 0x08, 0x01, 0x01, 0xDF, 0xA6, 0x40, 0xE3, 0x15, 0x49, 0xF2, 0xBB]
#key_word = [0xAA, 0x38, 0x08, 0x00, 0x01, 0xAD, 0x18, 0xB9, 0xAC, 0xE5, 0xC0, 0xBA, 0xBB]
#auth_word_sector1 = [0xAA, 0x34, 0x02, 0x00, 0x01, 0xE1, 0xBB]
auth_sector1 = [0xAA, 0x34, 0x02, 0x01, 0x01, 0xE2, 0xBB]
auth_sector4 = [0xAA, 0x34, 0x02, 0x01, 0x04, 0xE5, 0xBB]
auth_sector5 = [0xAA, 0x34, 0x02, 0x01, 0x05, 0xE6, 0xBB]
secter1_block04 = [0xAA, 0x36, 0x01, 0x04, 0xE5, 0xBB]
secter1_block05 = [0xAA, 0x36, 0x01, 0x05, 0xE6, 0xBB]
secter1_block06 = [0xAA, 0x36, 0x01, 0x06, 0xE7, 0xBB]
secter4_block10 = [0xAA, 0x36, 0x01, 0x10, 0xF1, 0xBB]
secter4_block11 = [0xAA, 0x36, 0x01, 0x11, 0xF2, 0xBB]
secter4_block12 = [0xAA, 0x36, 0x01, 0x12, 0xF3, 0xBB]
secter5_block14 = [0xAA, 0x36, 0x01, 0x14, 0xF5, 0xBB]
secter5_block15 = [0xAA, 0x36, 0x01, 0x15, 0xF6, 0xBB]
secter5_block16 = [0xAA, 0x36, 0x01, 0x16, 0xF7, 0xBB]
rats_card = [0xAA, 0x39, 0x01, 0x00, 0xE4, 0xBB]
dict={}
def open_serial():
    plist = list(serial.tools.list_ports.comports())
    if len(plist) <= 0:
        print("the serial port can't find")
    else:
        plist_0 = list(plist[0])
        serial_name = plist_0[0]
        return serial.Serial(serial_name, 115200, timeout=60)
        # print serialFd.portstr
        #print("check which[%s] port was really used>" % serialFd.name)
        # strInput = raw_input('enter some words:')

def pack_cmd(comannd_str):
    return struct.pack("%dB" % len(comannd_str), *comannd_str)

def beep(serialfd,beep_word):
    dat=pack_cmd(beep_word)
    serialfd.write(dat)
    serialFd.read(7)


def search_card(serialfd,find_card):
    list = []
    dat = pack_cmd(find_card)
    serialfd.write(dat)
    rcv=serialFd.read(10)
    reback_data=''.join(['%02X' % b for b in rcv])
    print(reback_data)
    back_data = reback_data[6:14]
    if back_data == '00000000':
        return False
    else:
        cardid_WG34=reback_data[12:14]+reback_data[10:12]+reback_data[8:10]+reback_data[6:8]
        cardid_WG34=int("0x"+cardid_WG34,16)#4位物理卡号
        cardid_WG26=reback_data[10:12]+reback_data[8:10]+reback_data[6:8]
        cardid_WG26=int("0x"+ cardid_WG26,16)#3位物理卡号
        list.append(str(cardid_WG34))
        list.append(str(cardid_WG26))
        return list

def halt_read(serialfd,halt_word):
    dat = pack_cmd(halt_word)
    serialfd.write(dat)
    serialFd.read(7)

def load_key(serialfd,key_word):
    dat = pack_cmd(key_word)
    serialfd.write(dat)
    rcv = serialFd.read(7)
    reback_data=''.join(['%02X' % b for b in rcv])
    print(reback_data)
    #back_data = rcv[3:5].encode('hex').upper()
    back_data = reback_data[6:10]
    if back_data == '0000':
        return True
    else:
        print("load_key failed")
        exit(10001)

def auth_key(serialfd,auth_word_sector):
    dat = pack_cmd(auth_word_sector)
    serialfd.write(dat)
    rcv = serialFd.read(7)
    reback_data=''.join(['%02X' % b for b in rcv])
    print(reback_data)
    #back_data = rcv[3:5].encode('hex').upper()
    back_data = reback_data[6:10]
    if back_data == '0000':
        return True
    else:
        print("auth_key failed")
        exit(10002)

def read_sector(serialfd,auth_word_sector):
    load_key(serialfd,key_word)
    auth_key(serialfd,auth_word_sector)

def read_block(serialfd, block):
    dat = pack_cmd(block)
    serialfd.write(dat)
    data = serialFd.read(22)
    reback_data=''.join(['%02X' % b for b in data])
    print(reback_data)
    return reback_data
	
def read_card_water_id(serialfd, block):
    dat = pack_cmd(block)
    serialfd.write(dat)
    data = serialFd.read(22)
    reback_data=''.join(['%02X' % b for b in data])
    cardid_WG26=reback_data[10:12]+reback_data[8:10]+reback_data[6:8]
    cardid_WG26=int("0x"+ cardid_WG26,16)#3位物理卡号
    return str(cardid_WG26)

def read1_block(serialfd,block):
    dat = pack_cmd(block)
    serialfd.write(dat)
    rcv = serialFd.read(22)
    reback_data = rcv[3:6][::-1].encode('hex').upper()
    print ("卡流水号：" + str(int("0x" + reback_data, 16)))
    back_data = rcv[3:19].encode('hex').upper()
    print ("卡类："+str(back_data[-1]))
    print ("有效期：" + "20" + str(back_data[6:8]) + "年" + str(back_data[9:10]) + "月" + str(back_data[10:11]) + "日")
    if (int(back_data[12:14]) ==41):
        print("男")
    else:
        print(back_data[12:14])
        print("女")
    print ("身份证号码：" + str(back_data[14:36]))
    print(back_data)
def read_card_sector(serial_handle, sector,block1,block2,block3):
    dic = {}
    if sector == 1:
        if find_m1_card(serial_handle,1) == True:
            if auth_key(serial_handle, auth_sector1)==True:
                data_block1 = read_block(serial_handle, block1)
                cardid_hex =  data_block1[3:6][::-1].encode('hex').upper()
                dic["cardID"]=str(int("0x" + cardid_hex, 16))
                print ("卡流水号：" + str(int("0x" + cardid_hex, 16)))
                data_sub =  data_block1[3:19].encode('hex').upper()
                print ("有效期："+ "20"+str(data_sub[6:8])+"年"+str(data_sub[9:10])+"月"+str(data_sub[10:11])+"日")
                if(data_sub[11:12]=="41"):
                    print("男")
                else:
                    print("女")
                print ("身份证号码：" + str(data_sub[14:36]))
                data_block2=read_block(serial_handle, block2)
                data_sub2 = data_block2[3:19].encode('hex').upper()
                print ("卡类：" + str(data_sub2[-1]))
                data_block3=read_block(serial_handle, block3)
                data_sub3 = data_block3[3:19].encode('hex').upper()

def find_m1_card(serialfd,show_card_num=0):
    data = search_card(serialfd)
    if (data != 0):
        if(show_card_num==1):
            print("卡物理号："+str(data))
    else:
        halt_read(serialfd)
        flag = 1
        while flag < 3:
            data = search_card(serialfd)
            if (search_card(serialfd) !=False ):
                print(data)
                beep(serialfd)
                break
            else:
                flag = flag + 1
                halt_read(serialfd)
        print("find card is null")
        beep(serialfd, 4)
        exit(2)
        return False
    # load keyword on RAM ,for M1 card
    if load_key(serialFd)!= 0:
        print("load key fialed")
        beep(serialFd, 4)
        exit(3)
        return False
    return True
def gbk_incode_to_hanzi(data):
    emp_name =""
    for i in range(0, len(data), 4):
        if data[i:i + 4] != '0000':
            hw = hex(int(str(int("0x" + data[i:i + 4], 16))[0:2]) + int("0xA0", 16))[2:4]
            lw = hex(int(str(int("0x" + data[i:i + 4], 16))[2:4]) + int("0xA0", 16))[2:4]# 汉字gbk内码转gbk编码
            emp_name = emp_name + hw + lw
            continue
        else:
            break
    return binascii.a2b_hex(emp_name).decode("GB2312").encode("utf-8")#gbk编码汉字
 
def cal_money(hex_vlue):
    value =hex_vlue[0:2] + hex_vlue[4:6]+hex_vlue[2:4]
    return locale.format("%.2f", int(value,16)/100, 1)
def cal_times(hex_vlue):
    value = hex_vlue[4:6] + hex_vlue[2:4] + hex_vlue[0:2]
    return int(value,16)
def cal_date(hex_vlue):
    value = hex_vlue[6:8] + hex_vlue[4:6] + hex_vlue[2:4] + hex_vlue[0:2]
    timeArray = time.localtime(int(value, 16))
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return str(otherStyleTime)
if __name__ == '__main__':
    serialFd = serial.Serial('COM4', 115200, timeout=60)
    dic={}
    secter_data = []
    ls=search_card(serialFd,find_card)
    dic['wg34']=ls[0]
    dic['wg26']=ls[1]
    print("10位卡号："+str(ls[0]))
    print("8位卡号："+str(ls[1]))
    read_sector(serialFd, auth_sector1)#读1号扇区
    print(read_card_water_id(serialFd, secter1_block04))
    #dic['cardid']=int(secter_data[0][3:6][::-1].encode('hex').upper(),16)
    #print("卡流水号："+str(dic['cardid']))#卡流水水号
    data = secter_data[0][3:19].encode('hex').upper()
    dic['end_date']='20'+str(data[6:8])+'-'+str(data[8:10])+'-'+str(data[10:12])
    print("卡有效日期："+dic['end_date'])
    dic['id']=str(data[14:36])
    print ("持卡人身份证号码："+str(dic['id']))
    if (data[13:14] == "1"):
        dic['sex']='男'
    else:
        dic['sex']='女'
    print("持卡人性别："+str(dic['sex']))
    del secter_data[0]
    secter_data.append(read_block(serialFd, secter1_block5))
    data = str(secter_data[0][7:19].encode('hex').upper())
    dic['empno']=binascii.a2b_hex(data).replace(" ","")
    print("持卡人工号："+str(dic['empno']))
    del secter_data[0]
    secter_data.append(read_block(serialFd, secter1_block6))
    data = str(secter_data[0][3:19].encode('hex').upper())
    username=gbk_incode_to_hanzi(data)
    dic['username']=username
    print("持卡人姓名："+str(dic['username']))
    beep(serialFd, beep_word)
    del secter_data[0]
    read_sector(serialFd, auth_sector4)#读4号扇区
    secter_data.append(read_block(serialFd, secter4_block10))
    dic['cardclass']=int(secter_data[0][4:5].encode('hex').upper())
    print ("卡类："+str(dic['cardclass']))
    data2=str(secter_data[0][10:13].encode('hex').upper())
    dic['cardmoney']=cal_money(data2)
    print("卡余额："+str(dic['cardmoney']))
    data3 = str(secter_data[0][14:18].encode('hex').upper())
    dic['posmoney']=cal_money(data3)
    print("最后一次消费："+dic['posmoney'])
    del secter_data[0]
    secter_data.append(read_block(serialFd, secter4_block11))
    data4 = str(secter_data[0][10:13].encode('hex').upper())
    dic['cardmoney1'] = cal_money(data4)
    print("备份区卡余额：" + str(dic['cardmoney1']))
    data5 = str(secter_data[0][14:18].encode('hex').upper())
    dic['daytotal'] = cal_money(data5)
    print("日累计额：" +dic['daytotal'] )
    data6=secter_data[0][3:6].encode('hex').upper()
    dic['usetimes']=cal_times(data6)
    print("卡使用次数："+str(dic['usetimes']))
    del secter_data[0]
    secter_data.append(read_block(serialFd, secter4_block12))
    data7=secter_data[0][15:19].encode('hex').upper()
    print(cal_date(data7))