#!usr/bin/python
#encoding=utf-8
import RPi.GPIO as GPIO
import time
#数码管显示
class TM1637:
    #0-9的数码管对应编码 列表
    segdata = [0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f]
    #0:-9:带dp显示的数码管对应编码 列表
    segdatadp = [0xbf,0x86,0xdb,0xcf,0xe6,0xed,0xfd,0x87,0xff,0xef]
    def __init__(self,CLK,DIO):
        self.CLK = CLK
        self.DIO = DIO
        self.init()
        
    #数据传输开始函数
    def start(self):
        GPIO.output(self.CLK,GPIO.HIGH)
        GPIO.output(self.DIO,GPIO.HIGH)
        GPIO.output(self.DIO,GPIO.LOW)
        GPIO.output(self.CLK,GPIO.LOW)
    #数据传输结束函数
    def stop(self):
        GPIO.output(self.CLK,GPIO.LOW)
        GPIO.output(self.DIO,GPIO.LOW)
        GPIO.output(self.CLK,GPIO.HIGH)
        GPIO.output(self.DIO,GPIO.HIGH)
    #发送bit(位)数据
    def write_bit(self,bit):
        GPIO.output(self.CLK,GPIO.LOW)
        if bit:
            GPIO.output(self.DIO,GPIO.HIGH)
        else:
            GPIO.output(self.DIO,GPIO.LOW)
        GPIO.output(self.CLK,GPIO.HIGH)
    #发送byte(字节)数据
    def write_byte(self,data):
        for i in range(0,8):
            #将1个字节的数据拆分成8个二进制位发送
            self.write_bit((data >> i) & 0x01)
        GPIO.output(self.CLK,GPIO.LOW)
        GPIO.output(self.DIO,GPIO.HIGH)
        GPIO.output(self.CLK,GPIO.HIGH)
        GPIO.setup(self.DIO,GPIO.IN)
        num = 0 
        #等待数码管将DIO电平拉低ACK
        while GPIO.input(self.DIO) and num < 10:
            num += 1
        GPIO.setup(self.DIO,GPIO.OUT)
    #控制单个数码管显示数字，(发送数码管显示寄存器地址+显示编码)    
    def write_data(self,addr,data):
        self.start()
        self.write_byte(addr)
        self.write_byte(data)
        self.stop()
    #发送参数设置信息
    def write_command(self,cmd):
        self.start()
        self.write_byte(cmd)
        self.stop()
    #控制数码管显示数字    
    def display(self,args):
        self.write_command(0x40) #写数据
        self.write_command(0x44) #固定地址
        self.write_data(0xc0,self.segdata[args[0]])
        self.write_data(0xc1,self.segdata[args[1]])
        self.write_data(0xc2,self.segdata[args[2]])
        self.write_data(0xc3,self.segdata[args[3]])
        self.write_command(0x88)#数码管显示开
    #控制数码管显示时间
    def display_Time(self,h_shi,h_ge,m_shi,m_ge,flag_dp):
        self.write_command(0x40) #写数据
        self.write_command(0x44) #固定地址
        self.write_data(0xc0,self.segdata[h_shi])
        if flag_dp:
            self.write_data(0xc1,self.segdata[h_ge])
        else:
            self.write_data(0xc1,self.segdatadp[h_ge])
        self.write_data(0xc2,self.segdata[m_shi])
        self.write_data(0xc3,self.segdata[m_ge])
        self.write_command(0x88)#数码管显示开
    #数码管GPIO初始化    
    def init(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.CLK,GPIO.OUT)
        GPIO.setup(self.DIO,GPIO.OUT)
        
'''
test = TM1637(5,6)
try:
    flag_dp = 1
    while 1:
        flag_dp ^= 1
        curtime = time.localtime()        
        h_shi = curtime[3]/10
        h_ge = curtime[3]%10
        m_shi = curtime[4]/10
        m_ge = curtime[4]%10
        print "before display_Time"
        test.display_Time(h_shi,h_ge,m_shi,m_ge,flag_dp)
        print "after"
except KeyboardInterrupt:
    pass
GPIO.cleanup()  
'''
'''
#example    显示当前时间
test = TM1637(5,6)
try:
    flag_dp = 1
    while 1:
        flag_dp ^= 1
        curtime = time.localtime()        
        h_shi = curtime[3]/10
        h_ge = curtime[3]%10
        m_shi = curtime[4]/10
        m_ge = curtime[4]%10
        test.display_Time(h_shi,h_ge,m_shi,m_ge,flag_dp)
        time.sleep(1)
except KeyboardInterrupt:
    pass
GPIO.cleanup()   
'''
