from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import RPi.GPIO as GPIO

in1 = 25
in2 = 24
in3 = 23
in4 = 22
enA = 12
enB = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enA,GPIO.OUT)
GPIO.setup(enB,GPIO.OUT)
p1=GPIO.PWM(enA,1000)
p2=GPIO.PWM(enB,1000)
p1.start(30)
p2.start(30)
GPIO.output(in1,GPIO.HIGH)
GPIO.output(in2,GPIO.HIGH)
GPIO.output(in3,GPIO.HIGH)
GPIO.output(in4,GPIO.HIGH)

camera = PiCamera()
camera.resolution = (640, 360)
camera.rotation = 180
rawCapture = PiRGBArray(camera, size=(640, 360))
time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    roi = image[200:250, 0:639]
    Blackline= cv2.inRange(roi, (0,0,0), (50,50,50))
    kernel = np.ones((3,3), np.uint8)
    Blackline = cv2.erode(Blackline, kernel, iterations=5)
    Blackline = cv2.dilate(Blackline, kernel, iterations=9)	
    img,contours, hierarchy = cv2.findContours(Blackline.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0 :
        x,y,w,h = cv2.boundingRect(contours[0])
        cv2.line(image, (x+(w/2), 200), (x+(w/2), 250), (255,0,0),3)
    cv2.imshow("original with line", image)
    rawCapture.truncate(0)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)