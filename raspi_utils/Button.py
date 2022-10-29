import RPi.GPIO as GPIO;

class Button:
    pin = 1;
    callback = None;

    def __init__(self, pin: int, callback=None):
        self.pin = pin;
        self.callback = callback;

        GPIO.setmode(GPIO.BCM);
        GPIO.setwarnings(False);

        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=callback, bouncetime=50)

    def cleanup(self):
        GPIO.cleanup(self.pin);
