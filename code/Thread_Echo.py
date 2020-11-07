#!/usr/bin/python
#encoding=utf-8
#超声波避障模块

#导入线程模块
import time, threading
import RPi.GPIO as GPIO
import TM1637
import Echo

class EchoObstacle (threading.Thread):
    __distance = 0  #当前探测距离
    def getDistance(self):
        return self.__distance
    #构造函数
    def __init__(self, echoPin, displayPin):
        super(EchoObstacle,self).__init__()
        #创建数码管显示对象，超声波探测对象
        self.__display = TM1637.TM1637(displayPin[0],displayPin[1])
        self.__echo = Echo.Echo(echoPin[0],echoPin[1])
        
        self.__flag = threading.Event()     #用于暂停线程的标识
        self.__flag.set()                   #设置为True
        self.__running = threading.Event()  #用于停止线程的标识
        self.__running.set()                #将running设置为True
        
    def run(self):
        print "th_echo running"
        while self.__running.isSet():
            print "echo running"
            #获取超声探测结果
            self.__echo.Measure()            
            print "measure"
            self.__distance = self.__echo.getDistance()
            #数码管显示探测结果
            distance = self.__echo.getListDistance()
            #print "before display"
            self.__display.display(distance)
            #print "after display"
            time.sleep(0.2)
            self.__flag.wait()          #为True时立即返回，为False时阻塞知道内部非标识位为True后返回  

    def pause(self):
        self.__flag.clear()     #设置为False，让线程阻塞
        print "echo thread pause"
    
    def resume(self):
        self.__flag.set()       #设置为True，让线程停止阻塞
        print "echo thread resume"
    
    def stop(self):
        self.__flag.set()       #将线程从暂停状态恢复，如果已经暂停的话
        self.__running.clear()  #设置为False
        print "echo thread stop"
#example
'''
th_Echo = EchoObstacle((14,15),(5,6))
th_Echo.start()
try:
    while True:
        pass
except KeyboardInterrupt:
    th_Echo.stop()
    GPIO.cleanup()
'''