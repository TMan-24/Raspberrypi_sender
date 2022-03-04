import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
TRIGGER1 = 18
ECHO1 = 5
MAX_TIME = 0.04
 
#set GPIO direction (IN / OUT)
GPIO.setup(TRIGGER1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)
 
def distance():
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
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()