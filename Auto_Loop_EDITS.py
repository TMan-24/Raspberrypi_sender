''' 
    Main programmers: Tony Anderson, Grant Yates
    Debugging/Acknowledgements: Joseph Miller, Casey Lee
    Date Created: 02/11/2022
    File Name: Auto_Loop.py
    
    Program Description: Uses Line Sensors for course 
    navigation via the control of two DC motors and Ultrasonic 
    sensors for barricade detection and assistance in turning 
    the vehicle when necessary.

    Legend:
        R = Right
        L = Left
        RM = Right Middle
        LM = Left Middle 
        en = Enable
        
        The Line Sensors work on a binary signal (0, 1)
        so when the sensors see white, it sends a 0, and
        when it sees black, it sends a 1 to the Raspberry Pi
'''

#Libraries
from dis import dis
from pickle import FALSE, TRUE     # pickle library for serializing data
import time                        # Main time library for TX/RX ultrasonic sensors
import math                        # Math library
from time import sleep             # time library for stopping execution of the code for a set amount of time
import RPi.GPIO as gpio            # RPi library for I/O purposes to Pi

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
GPIO26 = 26 #BUZZER PIN
GPIO27 = 27 #LM_SENSOR

# H-Bridge input control pins
RM_FORWARD = GPIO25   # blue
RM_BACKWARD = GPIO24  # green
LM_FORWARD =  GPIO23  # yellow
LM_BACKWARD = GPIO22  # orange

# Line Sensor pins
RM_SENSOR = GPIO4   # green
LM_SENSOR = GPIO27  # blue
R_SENSOR = GPIO15   # yellow
L_SENSOR = GPIO14   # purple

# H-bridge enable pins
EN_RM = GPIO12  # white
EN_LM = GPIO13  # black


# Pins for ultrasound sensor
TRIGGER1 = GPIO18 #Ultrasonic sensor 1 - Trigger
ECHO1 = GPIO5     #Ultrasonic sensor 1 - Echo
TRIGGER2 = GPIO19 #Ultrasonic sensor 2 - Trigger
ECHO2 = GPIO6     #Ultrasonic sensor 2 - Echo

# Helpful constants
Turn = True
Turn2 = True
LEFT_TURN = 10
FORWARD = 0
BACKWARD = 1
BRAKE = 2
LEFT_MOTOR = 0
RIGHT_MOTOR = 1
MAX_TIME = 0.04         # A timeout to exit loops for ultrasonic
TURN_AROUND_VALUE = 8   # Distance in cm for when to turn around
END_PROGRAM_VALUE1 = 19 # Distance in cm for ending wall
END_PROGRAM_VALUE2 = 20 # Distance in cm for ending wall (correcting for hardware error)
END_PROGRAM_VALUE3 = 21 # Error variable

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
        #while gpio.input(L_SENSOR) == gpio.HIGH:
            set_motor(LEFT_MOTOR, FORWARD)
            set_motor(RIGHT_MOTOR, BACKWARD)
            sleep(2)
    global Turn
    Turn = False
        #while gpio.input(RM_SENSOR) == gpio.HIGH:
            #set_motor(LEFT_MOTOR, BACKWARD)
            #set_motor(RIGHT_MOTOR, FORWARD)
    #else:
        # IF: leftmost sensor is OFF (LOW), then zero-degree turn left, until Rightmost sensor goes OFF (LOW) from being HIGH
        # turn until the right sensor is active (vehicle has turned far enough to cross the line)
        #while gpio.input(R_SENSOR) == gpio.HIGH:
        #    set_motor(LEFT_MOTOR, BACKWARD)
            #set_motor(RIGHT_MOTOR, FORWARD)
        #while gpio.input(LM_SENSOR) == gpio.HIGH:
            #set_motor(LEFT_MOTOR, FORWARD)
            #set_motor(RIGHT_MOTOR, BACKWARD)
    #global Turn
    #Turn = False

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
    sleep(0.001)
    return math.trunc(distance1)

def read_ultrasound2():

     # set Trigger to HIGH
    gpio.output(TRIGGER2, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    gpio.output(TRIGGER2, False)
    
    StartTime = time.time()
    # starting pulse
    timeout = StartTime + MAX_TIME
    # start StartTime
    while gpio.input(ECHO2) == 0 and StartTime < timeout:
        StartTime = time.time()
    
    StopTime = time.time()
    # stoping pulse
    timeout = StopTime + MAX_TIME
    # save time of arrival
    while gpio.input(ECHO2) == 1 and StopTime < timeout:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (17150 cm/s)
    # and divide by 2, because there and back
    distance2 = (TimeElapsed * 17150)
    sleep(0.001)
    return math.trunc(distance2)

# 180 Degree Turn
# This function will need to be improved by testing
def turn_around():
    set_motor(LEFT_MOTOR, FORWARD)
    set_motor(RIGHT_MOTOR, BACKWARD)
    sleep(3)
    while gpio.input(L_SENSOR) == gpio.HIGH and gpio.input(LM_SENSOR) == gpio.HIGH:
        set_motor(LEFT_MOTOR, FORWARD)
        set_motor(RIGHT_MOTOR, BACKWARD)
    global Turn2
    Turn2 = False
# Main program function
def main():
    
    print(" ############################################# ")
    print(" #                                           # ")
    print(" #                                           # ")
    print(" #        Welcome to Autonomous Robot        # ")
    print(" #                                           # ")
    print(" #                                           # ")
    print(" ############################################# ")
    print("\n")
    print("\n")
    
    # Begin initialization of the GPIO pins on the pi

    # Set warnings to false
    gpio.setwarnings(False)
    
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

    # Starting condition will be all four sensors are off (0), since starting square is all white
    # Check to see if the robot has come off the starting square
    print("Robot is now leaving white square")
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
        print("Robot is now Driving Straight")
        while TRUE:
            # State 1. continue straight - innermost sensors are on and outer sensors are on
            if gpio.input(R_SENSOR) == gpio.HIGH and gpio.input(L_SENSOR) == gpio.HIGH and gpio.input(RM_SENSOR) == gpio.HIGH and gpio.input(LM_SENSOR) == gpio.HIGH:
                # Set H-Bridge to go straight
                set_motor(RIGHT_MOTOR, FORWARD)
                set_motor(LEFT_MOTOR, FORWARD)
            # State 2. 90deg turn - either rightmost or leftmost sensor false (off) 
            elif gpio.input(R_SENSOR) == gpio.LOW:
                print("Right 90 Turn")
                turn_90(gpio.input(R_SENSOR))
                print("Robot is now Driving Straight")
            #elif gpio.input(L_SENSOR) == gpio.LOW:
            #    print("Left 90 Turn")
            #    turn_90(gpio.input(R_SENSOR))
            #    print("Robot is now Driving Straight")
            # State 3. correct back to line - use two middle sensors to determine
            elif gpio.input(RM_SENSOR) == gpio.LOW:
                set_motor(LEFT_MOTOR, FORWARD)
                set_motor(RIGHT_MOTOR, BACKWARD)
            else:
                set_motor(LEFT_MOTOR, BACKWARD)
                set_motor(RIGHT_MOTOR, FORWARD)
                
            # State 4. 180deg turn (turn around)
            if Turn == False:
                dist1 = read_ultrasound()
                dist2 = read_ultrasound2()
                #print ("Measured Distance1 = %.1f cm" % dist1)
                #print ("Measured Distance2 = %.1f cm" % dist2)
                if dist1 == TURN_AROUND_VALUE and dist2 == TURN_AROUND_VALUE:
                    print("180 Turn Around")
                    set_motor(LEFT_MOTOR, BACKWARD)
                    set_motor(RIGHT_MOTOR, BACKWARD)
                    sleep(0.5)
                    set_motor(RIGHT_MOTOR, BACKWARD)
                    set_motor(LEFT_MOTOR, BRAKE)
                    sleep(2)
                    set_motor(LEFT_MOTOR, BACKWARD)
                    set_motor(RIGHT_MOTOR, BACKWARD)
                    sleep(0.75)

                    turn_around()
                    print("Robot is now Driving Straight")
                if Turn == False and Turn2 == False:
                    if dist1 == LEFT_TURN and dist2 == LEFT_TURN:
                        set_motor(LEFT_MOTOR, BACKWARD)
                        set_motor(RIGHT_MOTOR, FORWARD)
                        sleep(2)

            

                #5. if we get back to starting position, stop program
                if gpio.input(RM_SENSOR) == gpio.LOW and gpio.input(LM_SENSOR) == gpio.LOW and gpio.input(R_SENSOR) == gpio.LOW and gpio.input(L_SENSOR) == gpio.LOW and ((dist1 and dist2) == END_PROGRAM_VALUE1 or (dist1 and dist2) == END_PROGRAM_VALUE2 or (dist1 and dist2) == END_PROGRAM_VALUE3):
                    # Stop motors and turn off all gpio settings
                    print("Going Home")
                    sleep(1.6)
                    set_motor(LEFT_MOTOR, BRAKE)
                    set_motor(RIGHT_MOTOR, BRAKE)
                    gpio.cleanup()
                    exit()
            
                elif gpio.input(RM_SENSOR) == gpio.HIGH and gpio.input(LM_SENSOR) == gpio.HIGH and gpio.input(R_SENSOR) == gpio.HIGH and gpio.input(L_SENSOR) == gpio.LOW and ((dist1 and dist2) == END_PROGRAM_VALUE1 or (dist1 and dist2) == END_PROGRAM_VALUE2 or (dist1 and dist2) == END_PROGRAM_VALUE3):
                    # Stop motors and turn off all gpio settings
                    print("Going Home")
                    sleep(1.6)
                    set_motor(LEFT_MOTOR, BRAKE)
                    set_motor(RIGHT_MOTOR, BRAKE)
                    gpio.cleanup()
                    exit()
            
                elif gpio.input(RM_SENSOR) == gpio.HIGH and gpio.input(LM_SENSOR) == gpio.HIGH and gpio.input(R_SENSOR) == gpio.LOW and gpio.input(L_SENSOR) == gpio.HIGH and ((dist1 and dist2) == END_PROGRAM_VALUE1 or (dist1 and dist2) == END_PROGRAM_VALUE2 or (dist1 and dist2) == END_PROGRAM_VALUE3):
                    # Stop motors and turn off all gpio settings
                    print("Going Home")
                    sleep(1.6)
                    set_motor(LEFT_MOTOR, BRAKE)
                    set_motor(RIGHT_MOTOR, BRAKE)
                    gpio.cleanup()
                    exit()
            
                elif gpio.input(RM_SENSOR) == gpio.HIGH and gpio.input(LM_SENSOR) == gpio.HIGH and gpio.input(R_SENSOR) == gpio.LOW and gpio.input(L_SENSOR) == gpio.LOW and ((dist1 and dist2) == END_PROGRAM_VALUE1 or (dist1 and dist2) == END_PROGRAM_VALUE2 or (dist1 and dist2) == END_PROGRAM_VALUE3):
                    # Stop motors and turn off all gpio settings
                    print("Going Home")
                    sleep(1.6)
                    set_motor(LEFT_MOTOR, BRAKE)
                    set_motor(RIGHT_MOTOR, BRAKE)
                    gpio.cleanup()
                    exit()
            
# program starts here. Boilerplate (reusable) python code for having a main function.
if __name__ == "__main__":
    main()