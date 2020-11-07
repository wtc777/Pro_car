#!/usr/bin/python
#encoding=utf-8
#红外寻迹模块
#黑色路径检知-模块指示灯灭，信号为1；
#非黑色路径检知-模块灯亮，信号为0；
#pin脚对应从右开始1,2,3,4 status = [右1，右2，右3，右4]
#导入线程模块
import time, threading
import RPi.GPIO as GPIO
import CarMotor
class ThreadTrace(threading.Thread):
    __status = [0,0,0,0]    #寻迹状态结果
    isRunning = False
    #构造函数
    def __init__(self,*args,**kwargs):
        super(ThreadTrace,self).__init__()
        print args
        #获取参数列表，初始化成员
        self.TracePin = args[0]
        self.LeftLed = args[1]
        self.RightLed = args[2]
        self.car = args[3]  #小车马达控制对象
        self.traceon = False#寻迹启用状态
        print self.TracePin,self.LeftLed,self.RightLed
        #树莓派针脚初始化
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TracePin[0],GPIO.IN)
        GPIO.setup(self.TracePin[1],GPIO.IN)
        GPIO.setup(self.TracePin[2],GPIO.IN)
        GPIO.setup(self.TracePin[3],GPIO.IN)
        GPIO.setup(self.RightLed,GPIO.OUT)
        GPIO.setup(self.LeftLed,GPIO.OUT)
        GPIO.output(self.RightLed,GPIO.LOW)
        GPIO.output(self.LeftLed,GPIO.LOW)
        #线程相关初始化
        self.__flag = threading.Event()     #用于暂停线程的标识
        self.__flag.set()                   #设置为True
        self.__running = threading.Event()  #用于停止线程的标识
        self.__running.set()                #将running设置为True
    
    #读取更新寻迹状态
    def read_status(self):
        self.__status[0] = GPIO.input(self.TracePin[0])
        self.__status[1] = GPIO.input(self.TracePin[1])
        self.__status[2] = GPIO.input(self.TracePin[2])
        self.__status[3] = GPIO.input(self.TracePin[3])
        
    def Ledon(self,left,right):
        GPIO.output(self.LeftLed,left)
        GPIO.output(self.RightLed,right)
        
    #多线程操作函数
    def run(self):
        print "trace thread start"
        
        while self.__running.isSet():
            print "trace running"
            self.isRunning = True
            #线程操作部分
            self.read_status()
            '''
            #print self.__status
            if self.__status == [0,1,1,0] or self.__status == [1,1,1,1]:
                #print "直行"
                self.car.forward()
                self.Ledon(0,0)
            elif self.__status == [0,0,0,0] :
                #print "停止"
                #print self.__status
                self.car.carStop()
                self.Ledon(0,0)
            elif self.__status == [0,0,1,0] or self.__status == [0,1,0,1] or self.__status == [0,0,1,1] or self.__status == [0,0,0,1]:                
                print "左转"
                self.car.turnLeft(30)
                print self.__status
                self.Ledon(1,0)
            elif self.__status == [0,1,0,0] or self.__status == [1,0,1,0] or self.__status == [1,1,0,0] or self.__status == [1,0,0,0]:
                print "右转"
                print self.__status
                self.car.turnRight(30)
                self.Ledon(0,1)
            '''
            if self.__status == [0,0,0,0] or self.__status == [0,1,1,0]:
                #print "直行"
                self.car.forward()
                self.Ledon(0,0)
            elif self.__status == [1,1,1,1]:
                #print "停止"
                #print self.__status
                self.car.carStop()
                self.Ledon(0,0)
            elif self.__status == [0,0,1,0]:
                #print "小左转"
                #print self.__status
                self.car.turnLeft(20)
                self.Ledon(1,0)
            elif self.__status == [0,0,0,1]:
                #print "大左转"
                #print self.__status
                self.car.turnLeft(30)
                self.Ledon(1,0)
            elif self.__status == [0,1,0,0]:
                #print "小右转"
                self.car.turnRight(20)
                #print self.__status
                self.Ledon(0,1)
            elif self.__status == [1,0,0,0]:
                #print "大右转"
                #print self.__status
                self.car.turnRight(30)                
                self.Ledon(0,1)
            #为True时立即返回，为False时阻塞知道内部非标识位为True后返回
            self.__flag.wait()          
            
    def pause(self):
        self.__flag.clear()     #设置为False，让线程阻塞
        '''
        if self.isRunning != False:
            print "trace thread pause"        
        '''
        print "trace thread pause"
        time.sleep(0.1)
        self.isRunning = False
        self.car.carStop()
    
    def resume(self):
        self.__flag.set()       #设置为True，让线程停止阻塞
        '''
        if self.isRunning == False:
            print "trace thread resume"
        '''
        print "trace thread resume"
        self.isRunning = True
        
    def stop(self):
        self.__flag.set()       #将线程从暂停状态恢复，如果已经暂停的话
        self.__running.clear()  #设置为False
        print "trace thread stop"        
        time.sleep(0.1)
        self.car.carStop()  
        
'''
#example
car  = CarMotor.CarMotor(12,16,20,21)
car.carStop()
a = ThreadTrace((23,24,25,8),27,17,car)
a.start()
a.pause()
time.sleep(5)
a.resume()
time.sleep(5)
a.pause()
time.sleep(8)
a.resume()
time.sleep(3)
a.stop()
try:
    while True:
        pass
except KeyboardInterrupt:
    a.stop()
    GPIO.cleanup()
'''
