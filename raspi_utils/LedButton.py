import RPi.GPIO as GPIO;
import time;

from raspi_utils.Button import Button
from raspi_utils.Led import Led


class LedButton:
    eventTime = 0;
    name = "";
    button = None;
    led = None;
    state = "off";

    def __init__(self, name: str, ledPin: int, buttonPin: int, callback=None):
        self.name = name;
        self.led = Led(ledPin);
        self.callback = callback;
        self.button = Button(buttonPin, callback=lambda channel: self.ledButtonCallback(channel, self.led));

    def ledButtonCallback(self, channel, led):
        ieventTime = time.monotonic_ns();
        istate: str = "off";
        if GPIO.input(channel) == GPIO.HIGH:
            istate = "on";
        if self.state == istate:
            print ("Ignoring - Same state", self.state," == ", istate);
            return;
        if (ieventTime - self.eventTime) < 100000000:
            print("Ignoring - Too soon event ", (ieventTime - self.eventTime), "ns");
            return;
        print("Registering after ", (ieventTime - self.eventTime), "ns");
        self.eventTime = ieventTime;
        if istate == "on":
            led.on();
            self.callback(self, istate);
            self.state = istate;
        else:
            led.off();
            self.callback(self, istate);
            self.state = istate;

    def getLed(self) -> Led:
        return self.led;

    def getButton(self) -> Button:
        return self.button;

    def name(self) -> str:
        return self.name;

    def cleanup(self):
        self.button.cleanup();
        self.led.cleanup();
