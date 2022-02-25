from pickle import TRUE
import RPi.GPIO as gpio

in1 = 25
in2 = 24
in3 = 23
in4 = 22
Rightlinesensor = 4
Leftlinesensor = 27
enA = 12
enB = 13
temp1=1

gpio.setmode(gpio.BCM)
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
p1.start(45)
p2.start(45)

try:
    while 1:
        if gpio.input(Rightlinesensor):
            #Black
 #           print("right FORWARD")
            gpio.output(in1,gpio.HIGH)
            gpio.output(in2,gpio.LOW)
        else:
            #White
  #          print("right BACKWARDS")
            gpio.output(in1,gpio.LOW)
            gpio.output(in2,gpio.HIGH)
        if gpio.input(Leftlinesensor):
            #Black
   #         print("left FORWORDS")
            gpio.output(in3,gpio.HIGH)
            gpio.output(in4,gpio.LOW)
        else:
            #White
    #        print("left BACKWARDS")
            gpio.output(in3,gpio.LOW)
            gpio.output(in4,gpio.HIGH)

finally:
    #cleanup the gpio pins before ending
    gpio.cleanup()
