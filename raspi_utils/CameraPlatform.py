import time

from board import SCL, SDA
import busio

from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

class CameraPlatform:
    sweepXPlane = True;
    sweepYPlane = True;
    def __init__(self):
        self.i2c = busio.I2C(SCL, SDA);
        self.pca = PCA9685(self.i2c);
        self.pca.frequency = 50;
        self.xplane = servo.Servo(self.pca.channels[1], min_pulse=610, max_pulse=2660)
        self.xplane.angle = 0;
        self.yplane = servo.Servo(self.pca.channels[0], min_pulse=620, max_pulse=2620)
        self.yplane.angle = 0;
        self.sleepInterval = 0.03;
        self.lastSleep = 0.5;

    def shiftXPlane(self, shiftValue: int):
        self.sweepXPlane = False;
        step = 1;
        if(shiftValue<0):
            step = -1;
        startAngle = int(self.xplane.angle);
        endAngle = startAngle + shiftValue;
        if endAngle < 0:
            endAngle = 0;
        elif endAngle > 180:
            endAngle = 180;
        for i in range(startAngle, endAngle, step):
            self.xplane.angle = i
            time.sleep(self.sleepInterval)
        self.xplane.angle = endAngle;
        time.sleep(self.lastSleep);

    def shiftYPlane(self, shiftValue: int):
        self.sweepYPlane = False;
        step = 1;
        if(shiftValue<0):
            step = -1;
        startAngle = int(self.yplane.angle);
        endAngle = startAngle + shiftValue;
        if endAngle<0:
            endAngle = 0;
        elif endAngle>180:
            endAngle = 180;
        for i in range(startAngle, endAngle, step):
            self.yplane.angle = i
            time.sleep(self.sleepInterval)
        self.yplane.angle = endAngle;
        time.sleep(self.lastSleep);

    def scanXPlane(self):
        maxAngle = 180;
        startAngle = int(self.xplane.angle);
        for i in range(startAngle, maxAngle, 1):
            if not self.sweepXPlane:
                return;
            self.xplane.angle = i
            time.sleep(self.sleepInterval)
        self.xplane.angle = maxAngle;
        time.sleep(self.lastSleep);
        for i in range(maxAngle, 0, -1):
            if not self.sweepXPlane:
                return;
            self.xplane.angle = i
            time.sleep(self.sleepInterval)
        self.xplane.angle = 0;
        time.sleep(self.lastSleep);

    def scanYPlane(self):
        maxAngle = 180;
        startAngle = int(self.yplane.angle);
        for i in range(startAngle, maxAngle, 1):
            if not self.sweepYPlane:
                return;
            self.yplane.angle = i
            time.sleep(self.sleepInterval)
        self.yplane.angle = maxAngle;
        time.sleep(self.lastSleep);
        for i in range(maxAngle, 0, -1):
            if not self.sweepYPlane:
                return;
            self.yplane.angle = i
            time.sleep(self.sleepInterval)
        self.yplane.angle = 0;
        time.sleep(self.lastSleep);

    def scanArea(self):
        maxAngle = 180;
        toggle = 0;
        for i in range(0, maxAngle, 1):
            if not self.sweepYPlane:
                return;
            self.xplane.angle = i
            time.sleep(self.sleepInterval)
            if toggle == 0:
                startY = 0;
                endY = maxAngle;
                stepY = 1;
                toggle = 1;
            else:
                startY = maxAngle;
                endY = 0;
                stepY = -1;
                toggle = 0;
            for j in range(startY, endY, stepY):
                if not self.sweepYPlane:
                    return;
                self.yplane.angle = j
                time.sleep(self.sleepInterval)
            self.yplane.angle = endY;
            time.sleep(self.lastSleep);
        self.xplane.angle = maxAngle;
        time.sleep(self.lastSleep);

    def clean(self):
        self.sweepXPlane = False;
        self.sweepYPlane = False;
        xangle = int(self.xplane.angle);
        yangle = int(self.yplane.angle);
        print("Reset from xplane: ", xangle, " yplane: ", yangle);
        for i in range(xangle, 0, -1):
            self.xplane.angle = i
            time.sleep(self.sleepInterval)
        self.xplane.angle = 0;
        time.sleep(self.lastSleep);
        for i in range(yangle, 0, -1):
            self.yplane.angle = i
            time.sleep(self.sleepInterval)
        self.yplane.angle = 0;
        time.sleep(self.lastSleep);
        self.pca.deinit()
