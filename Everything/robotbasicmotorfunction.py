import RPi.GPIO as GPIO          
from time import sleep

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
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward rh-right lh-left l-low m-medium h-high e-exit")
print("\n")    

while(1):
    x=input()
    
    if x=='r':
        print("run")
        if(temp1==1):
         GPIO.output(in1,GPIO.HIGH)
         GPIO.output(in2,GPIO.LOW)
         GPIO.output(in3,GPIO.HIGH)
         GPIO.output(in4,GPIO.LOW)
         print("backward")
         x='z'
        else:
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.HIGH)
         GPIO.output(in3,GPIO.LOW)
         GPIO.output(in4,GPIO.HIGH)
         print("forward")
         x='z'


    elif x=='s':
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)
        x='z'

    elif x=='f':
        print("forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
        temp1=1
        x='z'

    elif x=='b':
        print("backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
        temp1=0
        x='z'
    
    elif x=="lh":
        print("left")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
    
    elif x=="rh":
        print("right")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)

    elif x=='l':
        print("low")
        p1.ChangeDutyCycle(25)
        p2.ChangeDutyCycle(25)
        x='z'

    elif x=='m':
        print("medium")
        p1.ChangeDutyCycle(50)
        p2.ChangeDutyCycle(50)
        x='z'

    elif x=='h':
        print("high")
        p1.ChangeDutyCycle(75)
        p2.ChangeDutyCycle(75)
        x='z'
     
    
    elif x=='e':
        GPIO.cleanup()
        break
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")
