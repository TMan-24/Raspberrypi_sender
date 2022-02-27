from pickle import TRUE
import RPi.GPIO as gpio

IN1 = 25
IN2 = 24
IN3 = 23
IN4 = 22
Rightmiddlelinesensor = 4
Leftmiddlelinesensor = 27
ENA = 12
ENB = 13
TEMP1=1

gpio.setmode(gpio.BCM)
gpio.setup(Rightmiddlelinesensor, gpio.IN)
gpio.setup(Leftmiddlelinesensor, gpio.IN)
gpio.setup(IN1,gpio.OUT)
gpio.setup(IN2,gpio.OUT)
gpio.setup(IN3,gpio.OUT)
gpio.setup(IN4,gpio.OUT)
gpio.setup(ENA,gpio.OUT)
gpio.setup(ENB,gpio.OUT)
gpio.output(IN1,gpio.LOW)
gpio.output(IN2,gpio.LOW)
gpio.output(IN3,gpio.LOW)
gpio.output(IN4,gpio.LOW)
p1=gpio.PWM(ENA,1000)
p2=gpio.PWM(ENB,1000)
p1.start(45)
p2.start(45)

try:
    while TRUE:
        if gpio.input(Rightmiddlelinesensor):
            #Black
 #           print("right FORWARD")
            gpio.output(IN1,gpio.HIGH)
            gpio.output(IN2,gpio.LOW)
        else:
            #White
  #          print("right BACKWARDS")
            gpio.output(IN1,gpio.LOW)
            gpio.output(IN2,gpio.HIGH)
        if gpio.input(Leftmiddlelinesensor):
            #Black
   #         print("left FORWORDS")
            gpio.output(IN3,gpio.HIGH)
            gpio.output(IN4,gpio.LOW)
        else:
            #White
    #        print("left BACKWARDS")
            gpio.output(IN3,gpio.LOW)
            gpio.output(IN4,gpio.HIGH)

finally:
    #cleanup the gpio pins before ending
    gpio.cleanup()
