#!usr/bin/python
#encoding=utf-8
import RPi.GPIO as GPIO
import time

class Echo:
    __Distance = 0.0#当前检测距离(私有成员)
    __listDistance = [0,0,0,0]#当前检测距离，按位分离存储到列表中
    
    #构造函数
    def __init__(self, echo, trig):
        #针脚初始化
        self.echo = echo
        self.trig = trig
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.echo,GPIO.IN)
        GPIO.setup(self.trig,GPIO.OUT,initial = GPIO.LOW)
    #存取器-获取当前检测距离
    def getDistance(self):
        return self.__Distance
    def getListDistance(self):
        return self.__listDistance
    #触发检测当前距离
    def Measure(self):
        #触发高电平信号
        GPIO.output(self.trig,GPIO.HIGH)
        #持续至少10微秒
        time.sleep(0.001)
        #超声波发送结束
        GPIO.output(self.trig,GPIO.LOW)
        #判断接收端引脚是否为低电平，等待低电平结束
        num = 0
        while GPIO.input(self.echo) == GPIO.LOW:
            num += 1
            if num > 1000:
                return 0
        #接收到高电平开始计时
        t1 = time.time()
        num = 0
        while GPIO.input(self.echo) == GPIO.HIGH:
            num +=1
            if num > 100000:
                return 0
        t2 = time.time()
        #计算距离
        #计算公式；测试距离 = 测试时间 * 声速（340m/s) / 2
        self.__Distance = (t2 - t1) * 340 / 2 * 1000
        self.__Distance = int(self.__Distance)
        if self.__Distance >= 9999:
            self.__Distance = 9999#判断探测结果是否超范围
        self.__listDistance = \
        [self.__Distance/1000,self.__Distance/100%10,self.__Distance/10%10,self.__Distance%10]
'''
#example
test = Echo(14,15)
try:
    while True:
        test.Measure()
        time.sleep(1)
        print "distance:%d mm" % test.getDistance()
        print test.getListDistance()
        print "---"
except KeyboardInterrupt:
    pass
GPIO.cleanup()
'''
