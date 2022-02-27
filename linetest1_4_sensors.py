from pickle import FALSE
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN) #left
GPIO.setup(15, GPIO.IN) #right
GPIO.setup(27, GPIO.IN) #left-middle
GPIO.setup(4, GPIO.IN) #right-middle
in1 = 25
in2 = 24
in3 = 23
in4 = 22
enA = 12
enB = 13
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enA,GPIO.OUT)
GPIO.setup(enB,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p1=GPIO.PWM(enA,1000)
p2=GPIO.PWM(enB,1000)
p1.start(25)
p2.start(25)
temp1 = 1

try:
    while 1:
        if gpio.input(14) and gpio.input(15) and gpio.input(4) and gpio.input(27):
            print("BLACK")
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
            GPIO.output(in3,GPIO.HIGH)
            GPIO.output(in4,GPIO.LOW)    
        else:
            print("WHITE")
        
finally:
    #cleanup the gpio pins before ending
    gpio.cleanup()
