import RPi.GPIO as GPIO;
import time;

class ColorLed:
    on = GPIO.HIGH;
    off = GPIO.LOW;
    colors = {
        "red": [on, off, off],
        "green": [off, on, off],
        "blue": [off, off, on],
        "yellow": [on, on, off],
        "purple": [on, off, on],
        "cyan": [off, on, on],
        "white": [on, on, on],
        "black": [off, off, off],
        "off": [off, off, off]
    };

    colorPin = [0, 0, 0];

    def __init__(self, redPin: int, greenPin: int, bluePin: int):
        self.colorPin = [redPin, greenPin, bluePin];

        GPIO.setmode(GPIO.BCM);
        GPIO.setwarnings(False);

        GPIO.setup(redPin, GPIO.OUT);
        GPIO.setup(greenPin, GPIO.OUT);
        GPIO.setup(bluePin, GPIO.OUT);

    def color(self, color):
        colorValue = ColorLed.colors[color];
        for pin in range(0, 3):
            GPIO.output(self.colorPin[pin], colorValue[pin]);

    def cycle(self, sleepTime):
        for color, colorValue in ColorLed.colors.items():
            print("Color: ", color);
            for pin in range(0, 3):
                GPIO.output(self.colorPin[pin], colorValue[pin]);
            time.sleep(sleepTime);
        self.off();

    def off(self):
        colorValue = ColorLed.colors["off"];
        for pin in range(0, 3):
            GPIO.output(self.colorPin[pin], colorValue[pin]);