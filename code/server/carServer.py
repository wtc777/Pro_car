#!usr/bin/python
#encoding=utf-8
import socket
import  CarMotor
import Thread_Trace,Thread_Echo,Thread_Logic,SG90
import time
import RPi.GPIO as GPIO
global Opemode
Opemode=False  #全局变量-手自动模式-True自动模式，False手动模式
global carMotor 
carMotor = CarMotor.CarMotor(12,16,20,21)#创建小车马达控制类
carMotor.setSpeed(20)
Red=22
Green=27
Blue=10
Beep=4
#搭建python服务器端
'''
1 创建套接字    socket
2 绑定          bind
3 监听          listen
4 接受          accept
5 通信          send/recv
'''
#初始化led灯
def init_LED():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Red,GPIO.OUT)
    GPIO.setup(Green,GPIO.OUT)
    GPIO.setup(Blue,GPIO.OUT)
    GPIO.setup(Beep,GPIO.OUT)

    GPIO.output(Red,GPIO.LOW)
    GPIO.output(Green,GPIO.LOW)
    GPIO.output(Blue,GPIO.LOW)
    GPIO.output(Beep,GPIO.HIGH)
#手动驾驶模式
def Mode_manual(text,th_logic):

    global carMotor
    if text.find("Redon=1") != -1:
        print "红灯开"
        GPIO.output(Red,GPIO.HIGH)
    elif text.find("Redon=0") != -1:
        print "红灯关"
        GPIO.output(Red,GPIO.LOW)
    elif text.find("Greenon=1") != -1:
        print "绿灯开"
        GPIO.output(Green,GPIO.HIGH)
    elif text.find("Greenon=0") != -1:
        print "绿灯关"
        GPIO.output(Green,GPIO.LOW)
    elif text.find("Blueon=1") != -1:
        print "蓝灯开"
        GPIO.output(Blue,GPIO.HIGH)
    elif text.find("Blueon=0") != -1:
        print "蓝灯关"
        GPIO.output(Blue,GPIO.LOW)
    elif text.find("Beepon=1") != -1:
        print "蜂鸣开"
        GPIO.output(Beep,GPIO.LOW)
    elif text.find("Beepon=0") != -1:
        print "蜂鸣关"
        GPIO.output(Beep,GPIO.HIGH)
    elif text.find("forward=1") != -1 and not th_logic.ostacle:
        print "小车前进:"
        carMotor.forward()
    elif text.find("back=1") != -1 and not th_logic.ostacle:
        print "小车后退:"
        carMotor.back()
    elif text.find("turnleft=1") != -1 and not th_logic.ostacle:
        print "小车左转:"
        carMotor.turnLeft(carMotor.getSpeed())
    elif text.find("turnright=1") != -1 and not th_logic.ostacle:
        print "小车右转:"
        carMotor.turnRight(carMotor.getSpeed())
    elif text.find("stopcar=1") != -1:
        print "小车停止"
        carMotor.carStop()
#自动驾驶模式
def Mode_auto(text,th_Trace):
    if text.find("traceon=1") != -1:
        #寻迹模式线程唤醒
        th_Trace.resume()
        th_Trace.traceon = True
        print th_Trace.isRunning
        print "开启寻迹模式"
    elif text.find("traceon=0") != -1:
        #寻迹模式线程暂停        
        th_Trace.pause()
        th_Trace.traceon = False
        carMotor.carStop()
        print th_Trace.isRunning
        print "禁用寻迹模式"
        
#接受数据函数
def do_handle(clientsoc,th_Trace,th_logic):
    msg = "welcome..."
    global carMotor
    global Opemode
    while True:
        #time.sleep(1)
        text = clientsoc.recv(1024)        
        print "send to client.."
        print "字节数:" ,len(text)
        print text
        if(text == "end" or text == "" or len(text) == 0):
            print "client closed break loop"
            break
        clientsoc.send(msg)
        #clientsoc.send(msg)
        if text.find("connect=1") !=-1:
            print "微信小程序客户端已连接..."
        elif text.find("connect=0") !=-1:
            print "微信小程序客户端断开连接..."
        elif text.find("automode=1") != -1:
            #自动模式切换
            Opemode=True
            th_logic.setMode(Opemode)
            print "切换到自动模式"
        elif text.find("automode=0") != -1:
            #手动模式切换
            Opemode=False
            th_logic.setMode(Opemode)
            #th_Trace.pause()#暂停寻迹线程
            print "切换到手动模式"
        #速度修改操作
        elif text.find("maxspeed") != -1:
            print "speedchange=80"
            carMotor.setSpeed(85)
        elif text.find("midspeed") != -1:
            print "speedchange=45"
            carMotor.setSpeed(45)
        elif text.find("minspeed") != -1:
            print "speedchange=25"
            carMotor.setSpeed(25)            
        elif Opemode:#自动模式功能判定
            Mode_auto(text,th_Trace)            
        elif not Opemode:#手动模式功能判定
            print Opemode
            Mode_manual(text,th_logic)
    clientsoc.close()
    print "客户端已关闭..."
    
#调用针脚初始化函数
init_LED()    
#创建线程对象
sg_echo = SG90.SG90(18)                             #创建舵机控制对象
sg_echo.turn(90)                                    #超声波探测部初始化正前方
th_Trace = Thread_Trace.ThreadTrace((23,24,25,8),27,17,carMotor)#寻迹线程对象创建
th_Echo = Thread_Echo.EchoObstacle((14,15),(5,6))   #超声探测线程对象创建
th_Echo.start()                                     #开启超声探测功能
th_Trace.start()
th_Trace.pause()
carMotor.carStop()
time.sleep(1)
th_logic = Thread_Logic.ThreadLogic(th_Trace,th_Echo,carMotor,sg_echo,250,Beep)#创建避障逻辑判定线程对象
th_logic.start()#开启避障逻辑判定线程

#建立服务器端
#创建套接字
serversoc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#设置套接字选项，解决地址重复绑定问题
serversoc.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
#绑定主机地址
hostname = "raspberrypi.local"
hostIP = socket.gethostbyname(hostname)
hostPort = 8800
serversoc.bind((hostIP,hostPort))
print hostIP,hostPort
#监听
serversoc.listen(5)
#接受
try:
    while True:
        clientsoc,addr = serversoc.accept()
        print clientsoc,addr
        do_handle(clientsoc,th_Trace,th_logic)
except KeyboardInterrupt:
    pass
    #关闭线程
th_Trace.stop()
th_Echo.stop()
th_logic.stop()
carMotor.carStop()
GPIO.cleanup()
    
