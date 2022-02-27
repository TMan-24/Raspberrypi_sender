from pickle import TRUE
from pickle import FALSE
from time import sleep
import RPi.GPIO as gpio

in1 = 25
in2 = 24
in3 = 23
in4 = 22
RightMiddlelinesensor = 4
LeftMiddlelinesensor = 27
Rightlinesensor = 15
Leftlinesensor = 14
enA = 12
enB = 13

gpio.setmode(gpio.BCM)
gpio.setup(RightMiddlelinesensor, gpio.IN)
gpio.setup(LeftMiddlelinesensor, gpio.IN)
gpio.setup(Rightlinesensor, gpio.IN)
gpio.setup(Leftlinesensor, gpio.IN)
gpio.setup(in1,gpio.OUT)
gpio.setup(in2,gpio.OUT)
gpio.setup(in3,gpio.OUT)
gpio.setup(in4,gpio.OUT)
gpio.setup(enA,gpio.OUT)
gpio.setup(enB,gpio.OUT)
gpio.output(in1,gpio.LOW)
gpio.output(in2,gpio.LOW)
gpio.output(in3,gpio.LOW)
gpio.output(in4,gpio.LOW)
p1=gpio.PWM(enA,1000)
p2=gpio.PWM(enB,1000)
p1.start(30)
p2.start(30)

try:
    while True:
        if gpio.input(RightMiddlelinesensor) == False:
            #when it sees white
            print("hi")
            gpio.output(in1,gpio.HIGH)
            gpio.output(in2,gpio.LOW)
            gpio.output(in3,gpio.HIGH)
            gpio.output(in4,gpio.LOW)
        else:
            if gpio.input(RightMiddlelinesensor):
                #Black
                print("right forward")
                gpio.output(in1,gpio.HIGH)
                gpio.output(in2,gpio.LOW)
            else:
                #White
                print("right backwards")
                gpio.output(in1,gpio.LOW)
                gpio.output(in2,gpio.HIGH)
            if gpio.input(LeftMiddlelinesensor):
                #Black
                print("left forward")
                gpio.output(in3,gpio.HIGH)
                gpio.output(in4,gpio.LOW)
            else:
                #White
                print("left backwards")
                gpio.output(in3,gpio.LOW)
                gpio.output(in4,gpio.HIGH)
                
                #right turn
            if gpio.input(Rightlinesensor) == False:
                #when it sees white
                print('hi')
                gpio.output(in1,gpio.LOW)
                gpio.output(in2,gpio.HIGH)
                gpio.output(in3,gpio.HIGH)
                gpio.output(in4,gpio.LOW)
                sleep(10) #this is to time the turn

                #left turn
            elif gpio.input(Leftlinesensor) == False:
                #when it sees white
                print('hi')
                gpio.output(in1,gpio.HIGH)
                gpio.output(in2,gpio.LOW)
                gpio.output(in3,gpio.LOW)
                gpio.output(in4,gpio.HIGH)
                sleep(10) #this is to time the turn


finally:
    #cleanup the gpio pins before ending
    gpio.cleanup()
