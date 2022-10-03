import RPi.GPIO as GPIO
import time
import numpy as np

servoPIN = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(2.5) # Initialization
time.sleep(1)
try:
  while True:
      for dt in np.arange(2.5, 12.75, 0.25):
        print("dt = ", dt);
        p.ChangeDutyCycle(dt);
        time.sleep(0.025)
        p.ChangeDutyCycle(0);
        time.sleep(0.01)
      time.sleep(5);
      for dt in np.arange(12.5, 2.25, -0.25):
        print("dt = ", dt);
        p.ChangeDutyCycle(dt);
        time.sleep(0.025)
        p.ChangeDutyCycle(0);
        time.sleep(0.01)
      time.sleep(5);

except KeyboardInterrupt:
    p.ChangeDutyCycle(2.5)
    time.sleep(2)
    p.ChangeDutyCycle(0);
    time.sleep(0.01)
    p.stop()
    GPIO.cleanup()