import RPi.GPIO as GPIO;
import time;

class Button:
    pin = 1;
    callback = None;

    def __init__(self, pin: int, callback=None):
        self.pin = pin;
        self.callback = callback;
        self.state = "off";

        GPIO.setmode(GPIO.BCM);
        GPIO.setwarnings(False);

        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=lambda channel: self.buttonEventHandler(channel))

    def buttonEventHandler(self, channel):
        if self.callback is None:
            return;
        istate: str = "off";
        print("Button - ", self.pin, " - ", GPIO.input(channel));
        if GPIO.input(channel) == GPIO.HIGH:
            istate = "on";
        # Using bouncetime on the button
        if self.state == istate:
            print("Ignoring - Same state", self.state, " == ", istate);
            return;
        time.sleep(1 / 1000);
        if (GPIO.input(channel) == GPIO.HIGH and istate != "on") or (GPIO.input(channel) == GPIO.LOW and istate != "off"):
            print("Ignoring - State changed since last checked ");
            return;
        if istate == "on":
            self.callback(self, channel);
            self.state = istate;
        else:
            self.callback(self, channel);
            self.state = istate;


    def cleanup(self):
        GPIO.cleanup(self.pin);
