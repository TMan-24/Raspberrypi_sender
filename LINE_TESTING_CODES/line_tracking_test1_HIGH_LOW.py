#Do our ultrasonic sensors have ADC's built in? If not, may need to purchase ADC or new sensors
from pickle import FALSE, TRUE #pickle library for serializing data
from time import sleep #time library for date/time types
import RPi.GPIO as gpio #RPi library for I/O purposes to Pi

# All GPIO sensor connections
GPIO4 = 4 #RM_SENSOR
GPIO5 = 5  #Ultrasonic_1 - Echo
GPIO6 = 6  #Ultrasonic_2 - Echo
GPIO12 = 12 #enA
GPIO13 = 13 #enB
GPIO14 = 14 #L_SENSOR
GPIO15 = 15 #R_SENSOR
GPIO18 = 18 #Ultrasonic_1 - Trigger 
GPIO19 = 19 #Ultrasonic_2 - Trigger
GPIO22 = 25 #LM_FORWARD
GPIO23 = 24 #LM_BACKWARD
GPIO24 = 23 #RM_FORWARD
GPIO25 = 22 #RM_BACKWARD
GPIO26 = 26 #FREE
GPIO27 = 27 #LM_SENSOR

# H-Bridge input control pins
RM_FORWARD = GPIO22 #in4, blue
RM_BACKWARD = GPIO23   #in3, green
LM_FORWARD =  GPIO24    #in2, yellow
LM_BACKWARD = GPIO25   #in1, orange

# Line Sensor pins
RM_SENSOR = GPIO4   #right middle sensor, green
LM_SENSOR = GPIO27  #left middle sensor, blue
R_SENSOR = GPIO15   #right sensor, yellow
L_SENSOR = GPIO14   #left sensor, purple

# H-bridge enable pins
EN_LM = GPIO12  #enA, white  
EN_RM = GPIO13  #enB, black

###### THIS WILL LIKELY BE CHANGED #######
# Pins for ultrasound sensor Assuming 4 bit ADC, add more gpio if needed
US_BIT0 = GPIO18 #Ultrasonic sensor 1 - Trigger
US_BIT1 = GPIO26 #Ultrasonic sensor 1 - Echo
US_BIT2 = GPIO19 #Ultrasonic sensor 2 - Trigger
US_BIT3 = GPIO6  #Ultrasonic sensor 2 - Echo


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
    ##set_motor(LEFT_MOTOR, FORWARD)
    ##set_motor(RIGHT_MOTOR, FORWARD)

# Set a PWM signal of 1000 for both motors
p1=gpio.PWM(EN_LM, 1000)
p2=gpio.PWM(EN_RM, 1000)

    # Start motors
p1.start(30) #motor speeds
p2.start(30)

    ###### THIS WILL BE DIFFERENT PROBABLY ######
    # Set up GPIO for ultrasonic sensor as 4 bit input
    # This will require multiple GPIO pins 
gpio.setup(US_BIT0, gpio.IN)
gpio.setup(US_BIT1, gpio.IN)
gpio.setup(US_BIT2, gpio.IN)
gpio.setup(US_BIT3, gpio.IN)

# helpful constants
FORWARD = 0
BACKWARD = 1
BRAKE = 2
LEFT_MOTOR = 0
RIGHT_MOTOR = 1
THRESHOLD_VALUE = 14 # TODO: determine what the actual threshold should be for ultrasaound
def set_motor(motor_num, state):

    print("I GOT TO SET MOTOR\n")
    print("motor num: ", motor_num, "\n")
    print("state: ", state, "\n")
    '''print(FORWARD)
    print(BACKWARD)
    print(BRAKE)
    print(LEFT_MOTOR)
    print(RIGHT_MOTOR)'''
    # determine which motor to set
    if motor_num == LEFT_MOTOR:
        if state == FORWARD:
            print("right motor FORWARD")
            # make right motor forward
            gpio.output(RM_FORWARD, gpio.HIGH)
            gpio.output(RM_BACKWARD, gpio.LOW)
        elif state == BACKWARD:
            print("right motor BACKWARD")
            # make right motor backward
            gpio.output(RM_FORWARD, gpio.LOW)
            gpio.output(RM_BACKWARD, gpio.HIGH)
        elif state == BRAKE:
            # make right motor brake
            print("right motor BRAKE")
            gpio.output(RM_FORWARD, gpio.LOW)
            gpio.output(RM_BACKWARD, gpio.LOW)
        else:
            print("Invalid direction parameter")

    elif motor_num == RIGHT_MOTOR:
        if state == FORWARD:
            # make left motor forward
            print("left motor forward")
            gpio.output(LM_FORWARD, gpio.HIGH)
            gpio.output(LM_BACKWARD, gpio.LOW)
        elif state == BACKWARD:
            # make left motor backward
            print("left motor backward")
            gpio.output(LM_FORWARD, gpio.LOW)
            gpio.output(LM_BACKWARD, gpio.HIGH)
        elif state == BRAKE:
            # make right motor brake
            print("left motor BRAKE")
            gpio.output(LM_FORWARD, gpio.LOW)
            gpio.output(LM_BACKWARD, gpio.LOW)
        else:
            print("Invalid direction parameter")

    else:
        print("Invalid motor paramter")
    

'''def read_ultrasound():
    # convert binary to decimal. bit*2^0 + bit*2^1 + bit*2^2 + bit*2^3
    return (1 * gpio.input(US_BIT0)) + (2 * gpio.input(US_BIT1)) + (4 * gpio.input(US_BIT2)) + (8 * gpio.input(US_BIT3))
'''
# 90 Degree Turn
# This function will need to be improved by testing
def turn_90(direction):
    print("IM THE DIRECTION", direction)
    # LOW means that the right sensor was active so turn the vehicle 90 degrees right
    # IF: Rightmost sensor is ON (low), then zero-degree turn RIGHT, until Rightmost sensor goes OFF (HIGH), and then back ON (LOW)
    if direction == gpio.LOW:
        # turn until the left middle sensor is active (vehicle has turned far enough to cross the line)
        while gpio.input(L_SENSOR) == gpio.LOW:
            print("State 1 for turn90")
            set_motor(RIGHT_MOTOR, FORWARD)
            set_motor(LEFT_MOTOR, BRAKE)
    else:
        # IF: leftmost sensor is ON (low), then zero-degree turn left, until LEFTmost sensor goes OFF (HIGH), and then back ON (high)
        # turn until the right middle sensor is active (vehicle has turned far enough to cross the line)
        while gpio.input(RM_SENSOR) == gpio.LOW:
            print("turning left for 90")
            set_motor(RIGHT_MOTOR, BRAKE)
            set_motor(LEFT_MOTOR, FORWARD)
'''
# 180 Degree Turn
# This function will need to be improved by testing
def turn_around():
    # to turn 180deg we need left middle sensor to cross the line twice
    lm_crossed_line = 0
    lm_still_on_line = FALSE

    # turn one motor forward other backwards (0 point turn)
    while lm_crossed_line < 2:
        set_motor(LEFT_MOTOR, FORWARD)
        set_motor(RIGHT_MOTOR, BACKWARD)
        
        # prevent double counting of lm sensor by using dummy variable (will increment really fast while still over the line without and give preemptively kill turn)
        if gpio.input(LM_SENSOR) == gpio.LOW and not lm_still_on_line:
            lm_crossed_line = lm_crossed_line + 1 #increment left middle 
            lm_still_on_line = TRUE
        elif gpio.input(LM_SENSOR) == gpio.HIGH:
            lm_still_on_line = FALSE
        else:
            lm_still_on_line = TRUE
'''
def main():
    
    #begin initialization of the GPIO pins on the pi
    #init_gpio()
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
    '''
    # initialize motor to go forward
    #set_motor(LEFT_MOTOR, FORWARD)
    #set_motor(RIGHT_MOTOR, FORWARD)
    '''
    # Set a PWM signal of 1000 for both motors
    p1=gpio.PWM(EN_LM, 1000)
    p2=gpio.PWM(EN_RM, 1000)

    # Start motors
    p1.start(30) #motor speeds
    p2.start(30)

    ###### THIS WILL BE DIFFERENT PROBABLY ######
    # Set up GPIO for ultrasonic sensor as 4 bit input
    # This will require multiple GPIO pins 
    gpio.setup(US_BIT0, gpio.IN)
    gpio.setup(US_BIT1, gpio.IN)
    gpio.setup(US_BIT2, gpio.IN)
    gpio.setup(US_BIT3, gpio.IN)'''
    # Starting condition will be all four sensors are off (0), since starting square is all white
    # Check to see if the robot has come off the starting square
    while gpio.input(RM_SENSOR) == gpio.LOW and gpio.input(LM_SENSOR) == gpio.LOW and gpio.input(R_SENSOR) == gpio.LOW and gpio.input(L_SENSOR) == gpio.LOW:
        print("LEAVE")
        # Set H-Bridge to go straight
        set_motor(LEFT_MOTOR, FORWARD)
        set_motor(RIGHT_MOTOR, FORWARD)
        '''if gpio.input(L_SENSOR) == gpio.LOW:
            print("left: 0")
        else:
            print("left: 1")
        if gpio.input(LM_SENSOR) == gpio.LOW:
            print("left Middle: 0")
        else:
            print("left middle: 1")
        if gpio.input(RM_SENSOR) == gpio.LOW:
            print("Right Middle: 0")
        else:
            print("Right Middle: 1")
        if gpio.input(R_SENSOR) == gpio.LOW:
            print("Right: 0") 
        else:
            print("Right: 1")'''
        #continue
        sleep(2)
    if gpio.input(L_SENSOR) == gpio.LOW and gpio.input(LM_SENSOR) == gpio.LOW and gpio.input(RM_SENSOR) == gpio.LOW and gpio.input(R_SENSOR):
        main()
    else:
     # main logic of program
        while TRUE:
            if gpio.input(L_SENSOR) == gpio.LOW:
                print("left: 0")
            else:
                print("left: 1")
            if gpio.input(LM_SENSOR) == gpio.LOW:
                print("left Middle: 0")
            else:
                print("left middle: 1")
            if gpio.input(RM_SENSOR) == gpio.LOW:
                print("Right Middle: 0")
            else:
                print("Right Middle: 1")
            if gpio.input(R_SENSOR) == gpio.LOW:
                print("Right: 0") 
            else:
                print("Right: 1")
            #1. continue straight - innermost sensors are on and outer sensors are not on
            if gpio.input(R_SENSOR) == gpio.HIGH and gpio.input(L_SENSOR) == gpio.HIGH and gpio.input(RM_SENSOR) == gpio.HIGH and gpio.input(LM_SENSOR) == gpio.HIGH:
                # Set H-Bridge to go straight
                print("we are in state 1")
                set_motor(LEFT_MOTOR, FORWARD)
                set_motor(RIGHT_MOTOR, FORWARD)
            #2. 90deg turn - either rightmost or leftmost sensor false (off) 
            elif gpio.input(R_SENSOR) == gpio.LOW:
                print("we are in state 2")
                turn_90(gpio.input(R_SENSOR))
            #3. correct back to line - use two middle sensors to determine
            elif gpio.input(RM_SENSOR) == gpio.LOW:
                print("we are in state 3.1")
                set_motor(RIGHT_MOTOR, FORWARD)
                set_motor(LEFT_MOTOR, BACKWARD)
                #sleep(0.01)
            else:
                print("we are in state 3")
                set_motor(RIGHT_MOTOR, BACKWARD)
                set_motor(LEFT_MOTOR, FORWARD)
                #sleep(0.01)
                

            #4. 180deg turn (turn around) - additional logic needed to avoid 180deg turn at first 90deg turn
            #if read_ultrasound() < THRESHOLD_VALUE:
            #   turn_around()

            #5. if we get back to starting position, stop program
            #if gpio.input(RM_SENSOR) == gpio.LOW and gpio.input(LM_SENSOR) == gpio.LOW and gpio.input(R_SENSOR) == gpio.LOW and gpio.input(L_SENSOR) == gpio.LOW:
                # turn off all gpio settings
            #   set_motor(LEFT_MOTOR, BRAKE)
            #  set_motor(RIGHT_MOTOR, BRAKE)
            # print("we are in state 5")
            # gpio.cleanup()
                #exit()

# program starts here. Boilerplate (reusable) python code for having a main function.
if __name__ == "__main__":
    main()