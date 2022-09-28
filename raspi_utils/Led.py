import RPi.GPIO as GPIO;
import time;


class Led:
    pin = 1;

    def __init__(self, pin: int):
        self.pin = pin;

        GPIO.setmode(GPIO.BCM);
        GPIO.setwarnings(False);

        GPIO.setup(pin, GPIO.OUT);

    def blink(self, sleepTime):
        GPIO.output(self.pin, GPIO.HIGH);
        time.sleep(sleepTime);
        GPIO.output(self.pin, GPIO.LOW);

    def off(self):
        GPIO.output(self.pin, GPIO.LOW);

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH);

    def cleanup(self):
        GPIO.cleanup();