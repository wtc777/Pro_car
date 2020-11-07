#!/usr/bin/python
#encoding=utf-8
#避障逻辑处理模块

#导入线程模块
import time, threading
import RPi.GPIO as GPIO

class ThreadLogic (threading.Thread):
    __mode = False  #手自动模式标志
    def setMode(self,mode):
        self.__mode = mode
    #构造函数
    def __init__(self, th_trace, th_echo,carMotor,sg90, limit,Beep):
        super(ThreadLogic,self).__init__()        
        self.th_trace = th_trace    #寻迹线程对象
        self.th_echo = th_echo      #超声探测线程对象
        
        self.carMotor = carMotor    #小车马达控制对象
        self.sg90 = sg90    #获取舵机控制对象
        self.limit = limit  #获取避障判定下限
        self.ostacle = False#避障标志
        self.__Beep = Beep#获取蜂鸣器控制针脚编号
        self.__flag = threading.Event()     #用于暂停线程的标识
        self.__flag.set()                   #设置为True
        self.__running = threading.Event()  #用于停止线程的标识
        self.__running.set()                #将running设置为True
        
    def run(self):
        print "logic thread start"
        while self.__running.isSet():
            #获取超声探测结果
            self.__distance = self.th_echo.getDistance()            
            #判定是否遇到障碍
            if self.__distance > self.limit:
                self.ostacle = False
                if self.__mode and self.th_trace.isRunning == False and self.th_trace.traceon == True:
                    self.th_trace.resume()    #通畅,唤醒寻迹线程
            elif self.__distance < self.limit:                
                self.ostacle = True
                if self.__mode and self.th_trace.isRunning == True: #自动模式
                    self.th_trace.pause()   #暂停寻迹线程
                    #蜂鸣提示1秒
                    GPIO.output(self.__Beep,GPIO.LOW)
                    time.sleep(1)
                    GPIO.output(self.__Beep,GPIO.HIGH)
                    time.sleep(1)
                elif not self.__mode:#手动模式，调用舵机，左右转动寻找通路
                    #遇到障碍，小车制动，
                    self.carMotor.carStop()
                    #蜂鸣提示1秒
                    GPIO.output(self.__Beep,GPIO.LOW)
                    time.sleep(1)
                    GPIO.output(self.__Beep,GPIO.HIGH)
                    time.sleep(1)
                    #左转获取距离
                    self.sg90.turn(180)
                    time.sleep(0.5)
                    leftDis = self.th_echo.getDistance()
                    #右转获取距离
                    self.sg90.turn(0)
                    time.sleep(0.5)
                    RightDis = self.th_echo.getDistance()
                    #判断左转or右转
                    if leftDis > self.limit or RightDis > self.limit:
                        if leftDis > RightDis:#小车左转
                            self.carMotor.turnLeft(35)
                            time.sleep(1)
                            self.carMotor.carStop()
                        else: #小车右转
                            self.carMotor.turnRight(35)
                            time.sleep(1)
                            self.carMotor.carStop()
                    self.sg90.turn(90)#舵机恢复正对前方状态   
                    print "left",leftDis,"right",RightDis,"limit",self.limit                    
            self.__flag.wait()          #为True时立即返回，为False时阻塞知道内部非标识位为True后返回  

    def pause(self):
        self.__flag.clear()     #设置为False，让线程阻塞
        print "logic thread pause"
    
    def resume(self):
        self.__flag.set()       #设置为True，让线程停止阻塞
        print "logic thread resume"
    
    def stop(self):
        self.__flag.set()       #将线程从暂停状态恢复，如果已经暂停的话
        self.__running.clear()  #设置为False
        print "logic thread stop"
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