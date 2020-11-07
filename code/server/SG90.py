#!usr/bin/python
#encoding=utf-8
import RPi.GPIO as GPIO
import time

class SG90:
    def __init__(self,ctrPin):
        self.ctrPin = ctrPin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ctrPin,GPIO.OUT)
        self.__p = GPIO.PWM(self.ctrPin,50)#设置频率50hz
        self.__p.start(0)   #开始PWM调制
    def turn(self, degree):
        self.__p.ChangeDutyCycle(2.5 + 10 * degree / 180) #设置舵机转动角度
        time.sleep(0.5)
        self.__p.ChangeDutyCycle(0)#归零
        time.sleep(0.2)
    def __del__(self):
        self.__p.stop()#对象销毁，停止pwm
'''
#example
test = SG90(18)
test.turn(0)
print "0"
test.turn(90)
print "90"
test.turn(180)
print "180"
'''