#!usr/bin/python
#encoding=utf-8
import RPi.GPIO as GPIO
import time
#小车操作模块

class CarMotor():
    __speed = 25#小车速度
    def setSpeed(self,speed):
        self.__speed = speed
    def getSpeed(self):
        return self.__speed
    def __init__(self, Lpin1, Lpin2, Rpin1, Rpin2):#**kwarg kewarg["Lpin1"]
        self.Lpin1 = Lpin1
        self.Lpin2 = Lpin2
        self.Rpin1 = Rpin1
        self.Rpin2 = Rpin2
#针脚初始化
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.Lpin1,GPIO.OUT)
        GPIO.setup(self.Lpin2,GPIO.OUT)
        GPIO.setup(self.Rpin1,GPIO.OUT)
        GPIO.setup(self.Rpin2,GPIO.OUT)

        GPIO.output(self.Lpin1,GPIO.LOW)
        GPIO.output(self.Lpin2,GPIO.LOW)
        GPIO.output(self.Rpin1,GPIO.LOW)
        GPIO.output(self.Rpin2,GPIO.LOW)

        self.Lp1 = GPIO.PWM(self.Lpin1,50)
        self.Rp1 = GPIO.PWM(self.Rpin1,50)
        self.Lp2 = GPIO.PWM(self.Lpin2,50)
        self.Rp2 = GPIO.PWM(self.Rpin2,50)
        self.Lp1.start(0)
        self.Lp2.start(0)
        self.Rp1.start(0)
        self.Rp2.start(0)
    #小车前进
    def forward(self):
        self.changeForspeed(self.__speed)
        self.changeBackspeed(0)
        #print self.__speed
    #调节反转轮子速度    
    def changeForspeed(self,speed):
        self.Lp2.ChangeDutyCycle(speed)
        self.Rp2.ChangeDutyCycle(speed)
    #调节正转轮子速度
    def changeBackspeed(self,speed):
        self.Lp1.ChangeDutyCycle(speed)
        self.Rp1.ChangeDutyCycle(speed)
    #小车后退
    def back(self):
        self.changeForspeed(0)
        self.changeBackspeed(self.__speed)    
    #小车小左转
    def turnmicoLeft(self,speed):
        self.Lp1.ChangeDutyCycle(0)
        self.Lp2.ChangeDutyCycle(speed-10)
        self.Rp1.ChangeDutyCycle(0)
        self.Rp2.ChangeDutyCycle(speed)
    #小车左转
    def turnLeft(self,speed):
        self.Lp1.ChangeDutyCycle(0)
        self.Lp2.ChangeDutyCycle(speed)
        self.Rp1.ChangeDutyCycle(speed)
        self.Rp2.ChangeDutyCycle(0)
    #小车小右转
    def turnmicroRight(self,speed):
        self.Lp1.ChangeDutyCycle(0)
        self.Lp2.ChangeDutyCycle(speed)
        self.Rp1.ChangeDutyCycle(0)
        self.Rp2.ChangeDutyCycle(speed-10)
    #小车右转
    def turnRight(self,speed):
        self.Lp1.ChangeDutyCycle(speed)
        self.Lp2.ChangeDutyCycle(0)
        self.Rp1.ChangeDutyCycle(0)
        self.Rp2.ChangeDutyCycle(speed)
    def carStop(self):
        self.Lp1.ChangeDutyCycle(0)
        self.Lp2.ChangeDutyCycle(0)
        self.Rp1.ChangeDutyCycle(0)
        self.Rp2.ChangeDutyCycle(0)
    #小车停止
    def stop(self):        
        self.Lp1.stop()
        self.Lp2.stop()
        self.Rp1.stop()
        self.Rp2.stop()
        GPIO.output(self.Lpin1,GPIO.LOW)
        GPIO.output(self.Lpin2,GPIO.LOW)
        GPIO.output(self.Rpin1,GPIO.LOW)
        GPIO.output(self.Rpin2,GPIO.LOW)
#example
'''
test = CarMotor(12,16,20,21)
test.setSpeed(30)

test.forward()
time.sleep(2)
test.back()
time.sleep(2)

#test.turnLeft(30)
#time.sleep(2)
test.turnRight(30)
time.sleep(2)
test.stop()
GPIO.cleanup()
'''