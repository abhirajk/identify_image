import RPi.GPIO as GPIO
import time
import numpy as np

servoPIN = 19
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz
p.start(2.5)  # Initialization
time.sleep(1)


def rotate180(step:int = 0.1):
    lowest = 2.5;
    highest = 12.75;
    dt = 2.5;
    endDt = highest;
    if step < 0:
        dt = highest;
        endDt = lowest;
    point1Sleep = 0.01;
    sleepAtZero = 0.001;
    sleepFor = point1Sleep * abs(step) / 0.1;
    print("Rotate 180 with step: ", step, " sleepFor: ", sleepFor, " sleepAtZero: ", sleepAtZero);
    while dt >= 2.5 and dt <= 12.75:
        print("dt = ", dt);
        p.ChangeDutyCycle(dt);
        time.sleep(sleepFor);
        p.ChangeDutyCycle(0);
        time.sleep(sleepAtZero);
        dt = dt + step;
    print("dt = ", endDt);
    p.ChangeDutyCycle(endDt);
    time.sleep(sleepFor);
    p.ChangeDutyCycle(0);
    time.sleep(sleepAtZero);
    print("Done Rotation");


try:
    while True:
        rotate180(0.1)
        time.sleep(5);
        rotate180(-0.1)
        time.sleep(5);

except KeyboardInterrupt:
    p.ChangeDutyCycle(2.5)
    time.sleep(2)
    p.ChangeDutyCycle(0);
    time.sleep(0.001)
    p.stop()
    GPIO.cleanup()
