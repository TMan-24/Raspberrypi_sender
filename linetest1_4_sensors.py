from pickle import FALSE
import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setup(14, gpio.IN) #left
gpio.setup(15, gpio.IN) #right
gpio.setup(27, gpio.IN) #left-middle
gpio.setup(4, gpio.IN) #right-middle

temp1 = 1

try:
    while 1:
        if gpio.input(14) and gpio.input(15) and gpio.input(4) and gpio.input(27):
            print("BLACK")
        else:
            print("WHITE")
        
finally:
    #cleanup the gpio pins before ending
    gpio.cleanup()
