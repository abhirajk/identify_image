import RPi.GPIO as GPIO;
import time;

from raspi_utils.Button import Button
from raspi_utils.Led import Led


class LedButton:
    name = "";
    button = None;
    led = None;
    state = "off";

    def __init__(self, name: str, ledPin: int, buttonPin: int, callback=None):
        self.name = name;
        self.led = Led(ledPin);
        self.led.off();
        self.callback = callback;
        self.button = Button(buttonPin, callback=lambda channel: self.ledButtonCallback(channel, self.led));

    def ledButtonCallback(self, channel, led):
        istate: str = "off";
        print ("Button - ", self.name, " - ", GPIO.input(channel));
        if GPIO.input(channel) == GPIO.HIGH:
            istate = "on";
        #Using bouncetime on the button
        if self.state == istate:
            print ("Ignoring - Same state", self.state," == ", istate);
            return;
        time.sleep(1/1000);
        if (GPIO.input(channel) == GPIO.HIGH and istate != "on") or (GPIO.input(channel) == GPIO.LOW and istate != "off"):
            print("Ignoring - State changed since last checked ");
            return;
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
