import RPi.GPIO as GPIO;
import time;

from raspi_utils.Button import Button
from raspi_utils.Led import Led


class LedButton:
    name = "";
    button = None;
    led = None;

    def __init__(self, name: str, ledPin: int, buttonPin: int, callback=None):
        self.name = name;
        self.led = Led(ledPin);
        self.led.off();
        self.callback = callback;
        self.button = Button(buttonPin, callback=self.ledButtonCallback);

    def ledButtonCallback(self, channel):
        istate: str = 0;
        if GPIO.input(channel) == GPIO.HIGH:
            istate = 1;
        if GPIO.input(channel) == GPIO.HIGH:
            self.led.on();
            self.callback(self, istate);
        else:
            self.led.off();
            self.callback(self, istate);

    def getLed(self) -> Led:
        return self.led;

    def getButton(self) -> Button:
        return self.button;

    def name(self) -> str:
        return self.name;

    def cleanup(self):
        self.button.cleanup();
        self.led.cleanup();
