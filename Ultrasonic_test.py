import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
TRIGGER1 = 18
ECHO1 = 5
TRIGGER2 = 19
ECHO2 = 6
MAX_TIME = 0.04
 
#set GPIO direction (IN / OUT)
GPIO.setup(TRIGGER1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)
GPIO.setup(TRIGGER2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)
 
def distance1():
    # set Trigger to HIGH
    GPIO.output(TRIGGER1, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(TRIGGER1, False)
    
    StartTime = time.time()
    timeout = StartTime + MAX_TIME
    # save StartTime
    while GPIO.input(ECHO1) == 0 and StartTime < timeout:
        StartTime = time.time()
    
    StopTime = time.time()
    timeout = StopTime + MAX_TIME
    # save time of arrival
    while GPIO.input(ECHO1) == 1 and StopTime < timeout:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance1 = (TimeElapsed * 17150)
 
    return distance1
 
def distance2():
    # set Trigger to HIGH
    GPIO.output(TRIGGER2, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(TRIGGER2, False)
    
    StartTime = time.time()
    timeout = StartTime + MAX_TIME
    # save StartTime
    while GPIO.input(ECHO2) == 0 and StartTime < timeout:
        StartTime = time.time()
    
    StopTime = time.time()
    timeout = StopTime + MAX_TIME
    # save time of arrival
    while GPIO.input(ECHO2) == 1 and StopTime < timeout:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance2 = (TimeElapsed * 17150)
 
    return distance2

if __name__ == '__main__':
    try:
        while True:
            dist1 = distance1()
            print ("Measured Distance1 = %.1f cm" % dist1)
            dist2 = distance2()
            print ("Measured Distance2 = %.1f cm" % dist2)
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()