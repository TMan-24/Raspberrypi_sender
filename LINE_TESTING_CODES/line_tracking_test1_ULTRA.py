''' 
    Programmers: Tony Anderson, Grant Yates
    Date Created: 02/11/2022
    File Name: Auto_Loop.py
    Program Description: Uses Line Sensors and Ultrasonic 
    sensors to control two DC motors to drive a metal constructed
    robot on a white centerend line track.

    Legend:
        R = Right
        L = Left
        RM = Right Middle
        LM = Left Middle 
        en = Enable
        
        The Line Sensors work on a binary signal (0, 1)
        so when the sensors see white, it sends a 0, and
        when it sees black, it sends a 1
'''
#Libraries
from pickle import FALSE, TRUE     #pickle library for serializing data
import time                        #Main time library for making ultrasonic sensors
import math
from time import sleep             #time library for stoping the code for a set amount of time
from turtle import delay, distance #time library for date/time types
import RPi.GPIO as gpio            #RPi library for I/O purposes to Pi

# All GPIO sensor connections
GPIO4 = 4   #RM_SENSOR
GPIO5 = 5   #Ultrasonic_1 - Echo
GPIO6 = 6   #Ultrasonic_2 - Echo
GPIO12 = 12 #enA
GPIO13 = 13 #enB
GPIO14 = 14 #L_SENSOR
GPIO15 = 15 #R_SENSOR
GPIO18 = 18 #Ultrasonic_1 - Trigger 
GPIO19 = 19 #Ultrasonic_2 - Trigger
GPIO22 = 22 #LM_FORWARD
GPIO23 = 23 #LM_BACKWARD
GPIO24 = 24 #RM_FORWARD
GPIO25 = 25 #RM_BACKWARD
GPIO26 = 26 #FREE
GPIO27 = 27 #LM_SENSOR

# H-Bridge input control pins
RM_FORWARD = GPIO25   #in4, blue
RM_BACKWARD = GPIO24  #in3, green #look into changing comments
LM_FORWARD =  GPIO23  #in2, yellow
LM_BACKWARD = GPIO22  #in1, orange

# Line Sensor pins
RM_SENSOR = GPIO4   #right middle sensor, green
LM_SENSOR = GPIO27  #left middle sensor, blue #look into changing comments
R_SENSOR = GPIO15   #right sensor, yellow
L_SENSOR = GPIO14   #left sensor, purple

# H-bridge enable pins
EN_LM = GPIO12  #enA, white  #look into changing comments
EN_RM = GPIO13  #enB, black


# Pins for ultrasound sensor
TRIGGER1 = GPIO18 #Ultrasonic sensor 1 - Trigger
ECHO1 = GPIO5     #Ultrasonic sensor 1 - Echo
TRIGGER2 = GPIO19 #Ultrasonic sensor 2 - Trigger
ECHO2 = GPIO6     #Ultrasonic sensor 2 - Echo

# helpful constants
FORWARD = 0
BACKWARD = 1
BRAKE = 2
LEFT_MOTOR = 0
RIGHT_MOTOR = 1
MAX_TIME = 0.04 # a timeout to exit loops for ultrasonic
THRESHOLD_VALUE = 5 #cm # TODO: determine what the actual threshold should be for ultrasaound

# Set pinout mode to Broadcom (board communication)
gpio.setmode(gpio.BCM)

# Line sensor setup as input digital pins
gpio.setup(RM_SENSOR, gpio.IN)
gpio.setup(LM_SENSOR, gpio.IN)
gpio.setup(R_SENSOR, gpio.IN)
gpio.setup(L_SENSOR, gpio.IN)

# Setup H-bridge inputs as output pins
gpio.setup(RM_FORWARD, gpio.OUT)
gpio.setup(RM_BACKWARD, gpio.OUT)
gpio.setup(LM_FORWARD, gpio.OUT)
gpio.setup(LM_BACKWARD, gpio.OUT)

# Set H-bridge Enable motor signals as output pins 
gpio.setup(EN_LM, gpio.OUT)
gpio.setup(EN_RM, gpio.OUT)

# initialize motor to go forward
#set_motor(LEFT_MOTOR, FORWARD)
#set_motor(RIGHT_MOTOR, FORWARD)

# Set a PWM signal of 1000 for both motors
p1=gpio.PWM(EN_LM, 1000)
p2=gpio.PWM(EN_RM, 1000)

# Start motors
p1.start(30) #motor speeds
p2.start(30)

# Set up GPIO for ultrasonic sensor
gpio.setup(TRIGGER1, gpio.OUT)
gpio.setup(TRIGGER2, gpio.OUT)
gpio.setup(ECHO1, gpio.IN)
gpio.setup(ECHO2, gpio.IN)

# Set_motor function - sets motor to forward/backward/brake
def set_motor(motor_num, state):
    # determine which motor to set
    if motor_num == RIGHT_MOTOR:
        if state == FORWARD:
            # make right motor forward
            gpio.output(RM_FORWARD, gpio.HIGH)
            gpio.output(RM_BACKWARD, gpio.LOW)
        elif state == BACKWARD:
            # make right motor backward
            gpio.output(RM_FORWARD, gpio.LOW)
            gpio.output(RM_BACKWARD, gpio.HIGH)
        elif state == BRAKE:
            # make right motor brake
            gpio.output(RM_FORWARD, gpio.LOW)
            gpio.output(RM_BACKWARD, gpio.LOW)
        else:
            print("Invalid direction parameter")

    elif motor_num == LEFT_MOTOR:
        if state == FORWARD:
            # make left motor forward
            gpio.output(LM_FORWARD, gpio.HIGH)
            gpio.output(LM_BACKWARD, gpio.LOW)
        elif state == BACKWARD:
            # make left motor backward
            gpio.output(LM_FORWARD, gpio.LOW)
            gpio.output(LM_BACKWARD, gpio.HIGH)
        elif state == BRAKE:
            # make left motor brake
            gpio.output(LM_FORWARD, gpio.LOW)
            gpio.output(LM_BACKWARD, gpio.LOW)
        else:
            print("Invalid direction parameter")

    else:
        print("Invalid motor paramter")
    

# 90 Degree Turn 
# This function will need to be improved by testing
def turn_90(direction):
    # LOW means that the right sensor was active so turn the vehicle 90 degrees right
    # IF: Rightmost sensor is OFF (LOW), then zero-degree turn RIGHT, until Leftmost sensor goes OFF (LOW) from being HIGH
    if direction == gpio.LOW:
        # turn until the left sensor is active (vehicle has turned far enough to cross the line)
        while gpio.input(L_SENSOR) == gpio.HIGH:
            set_motor(LEFT_MOTOR, FORWARD)
            set_motor(RIGHT_MOTOR, BACKWARD)
        while gpio.input(RM_SENSOR) == gpio.HIGH:
            set_motor(LEFT_MOTOR, BACKWARD)
            set_motor(RIGHT_MOTOR, FORWARD)
    #else:
        # IF: leftmost sensor is OFF (LOW), then zero-degree turn left, until Rightmost sensor goes OFF (LOW) from being HIGH
        # turn until the right sensor is active (vehicle has turned far enough to cross the line)
        #while gpio.input(R_SENSOR) == gpio.HIGH:
         #   set_motor(LEFT_MOTOR, BACKWARD)
          #  set_motor(RIGHT_MOTOR, FORWARD)
        #while gpio.input(LM_SENSOR) == gpio.HIGH:
            #set_motor(LEFT_MOTOR, FORWARD)
            #set_motor(RIGHT_MOTOR, BACKWARD)

# read_ultrasound function - sends a sound wave to calculate distances
def read_ultrasound():
     # set Trigger to HIGH
    gpio.output(TRIGGER1, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    gpio.output(TRIGGER1, False)
    
    StartTime = time.time()
    # starting pulse
    timeout = StartTime + MAX_TIME
    # start StartTime
    while gpio.input(ECHO1) == 0 and StartTime < timeout:
        StartTime = time.time()
    
    StopTime = time.time()
    # stoping pulse
    timeout = StopTime + MAX_TIME
    # save time of arrival
    while gpio.input(ECHO1) == 1 and StopTime < timeout:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (17150 cm/s)
    # and divide by 2, because there and back
    distance1 = (TimeElapsed * 17150)
    print(distance1)
    return math.trunc(distance1)

# 180 Degree Turn
# This function will need to be improved by testing
def turn_around():
    exit()
    # to turn 180deg we need left middle sensor to cross the line twice
    lm_crossed_line = 0
    lm_still_on_line = FALSE

    # turn one motor forward other backwards (0 point turn)
    while lm_crossed_line < 2:
        set_motor(RIGHT_MOTOR, FORWARD)
        set_motor(LEFT_MOTOR, BACKWARD)
        
        # prevent double counting of lm sensor by using dummy variable (will increment really fast while still over the line without and give preemptively kill turn)
        if gpio.input(LM_SENSOR) == gpio.LOW and not lm_still_on_line:
            lm_crossed_line = lm_crossed_line + 1 #increment left middle 
            lm_still_on_line = TRUE
        elif gpio.input(LM_SENSOR) == gpio.HIGH:
            lm_still_on_line = FALSE
        else:
            lm_still_on_line = TRUE
# Main program function
def main():
    
    #begin initialization of the GPIO pins on the pi

    '''# Set pinout mode to Broadcom (board communication)
    gpio.setmode(gpio.BCM)

    # Line sensor setup as input digital pins
    gpio.setup(RM_SENSOR, gpio.IN)
    gpio.setup(LM_SENSOR, gpio.IN)
    gpio.setup(R_SENSOR, gpio.IN)
    gpio.setup(L_SENSOR, gpio.IN)

    # Setup H-bridge inputs as output pins
    gpio.setup(RM_FORWARD, gpio.OUT)
    gpio.setup(RM_BACKWARD, gpio.OUT)
    gpio.setup(LM_FORWARD, gpio.OUT)
    gpio.setup(LM_BACKWARD, gpio.OUT)

    # Set H-bridge Enable motor signals as output pins 
    gpio.setup(EN_LM, gpio.OUT)
    gpio.setup(EN_RM, gpio.OUT)

    # Set a PWM signal of 1000 for both motors
    p1=gpio.PWM(EN_LM, 1000)
    p2=gpio.PWM(EN_RM, 1000)

    # Start motors
    p1.start(30) #motor speeds
    p2.start(30)

    # Set up GPIO for ultrasonic sensor
    gpio.setup(TRIGGER1, gpio.OUT)
    gpio.setup(TRIGGER2, gpio.OUT)
    gpio.setup(ECHO1, gpio.IN)
    gpio.setup(ECHO2, gpio.IN)'''

    # Starting condition will be all four sensors are off (0), since starting square is all white
    # Check to see if the robot has come off the starting square
    while gpio.input(RM_SENSOR) == gpio.LOW and gpio.input(LM_SENSOR) == gpio.LOW and gpio.input(R_SENSOR) == gpio.LOW and gpio.input(L_SENSOR) == gpio.LOW:
        # Set H-Bridge to go straight
        set_motor(RIGHT_MOTOR, FORWARD)
        set_motor(LEFT_MOTOR, FORWARD)
        sleep(1)
    # Checking for a special case (Right sensor goes high when all other sensors are still low)
    if gpio.input(L_SENSOR) == gpio.LOW and gpio.input(LM_SENSOR) == gpio.LOW and gpio.input(RM_SENSOR) == gpio.LOW and gpio.input(R_SENSOR):
        main()
    else:
     # main logic of program
        while TRUE:
            #1. continue straight - innermost sensors are on and outer sensors are on
            if gpio.input(R_SENSOR) == gpio.HIGH and gpio.input(L_SENSOR) == gpio.HIGH and gpio.input(RM_SENSOR) == gpio.HIGH and gpio.input(LM_SENSOR) == gpio.HIGH:
                # Set H-Bridge to go straight
                set_motor(RIGHT_MOTOR, FORWARD)
                set_motor(LEFT_MOTOR, FORWARD)
            #2. 90deg turn - either rightmost or leftmost sensor false (off) 
            elif gpio.input(R_SENSOR) == gpio.LOW:
                turn_90(gpio.input(R_SENSOR))
            #3. correct back to line - use two middle sensors to determine
            elif gpio.input(RM_SENSOR) == gpio.LOW:
                set_motor(LEFT_MOTOR, FORWARD)
                set_motor(RIGHT_MOTOR, BACKWARD)
            else:
                set_motor(LEFT_MOTOR, BACKWARD)
                set_motor(RIGHT_MOTOR, FORWARD)
                
            #4. 180deg turn (turn around) - additional logic needed to avoid 180deg turn at first 90deg turn
            if read_ultrasound() == THRESHOLD_VALUE: 
                print("value from sensor: ", read_ultrasound())
                print("value from sensor: ", THRESHOLD_VALUE)
                turn_around()

            #5. if we get back to starting position, stop program
            #if gpio.input(RM_SENSOR) == gpio.LOW and gpio.input(LM_SENSOR) == gpio.LOW and gpio.input(R_SENSOR) == gpio.LOW and gpio.input(L_SENSOR) == gpio.LOW:
                # turn off all gpio settings
            #   set_motor(LEFT_MOTOR, BRAKE)
            #   set_motor(RIGHT_MOTOR, BRAKE)
            #   print("we are in state 5")
            #   gpio.cleanup()
            #   exit()

# program starts here. Boilerplate (reusable) python code for having a main function.
if __name__ == "__main__":
    main()