import random
import time
from queue import Queue

import RPi.GPIO as GPIO
from raspi_utils.LedButton import LedButton
from sense_hat import SenseHat

from raspi_utils.SenseDetectDisplay import SenseDetectDisplay
import signal
import sys

sense = SenseHat();
print("Creating SenseDetectDisplay...")
display = SenseDetectDisplay(sense,shapeFilePath= "raspi_utils/data/game.png"
                             , shapeLabelFilePath= "raspi_utils/data/game.txt");
print("Created SenseDetectDisplay");


def sigint_handler(sig, frame):
    print('KeyboardInterrupt is caught');
    display.clear();
    GPIO.cleanup();
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)


def main(args: list[str]) -> None:
    try:
        blinkCount = 4;
        ledOrder = [];
        wrongs = [];

        def popLedOrder(ledButton, state):
            if len(ledOrder) > 0:
                if state == "on":
                    expected = ledOrder[0];
                    if expected != ledButton.name:
                        display.show("wrong");
                        wrongs.append(len(ledOrder));
                        time.sleep(1);
                        display.clear();
                    else:
                        display.show("correct");
                        time.sleep(1);
                        display.clear();
                        del ledOrder[0];
                        if len(ledOrder) == 0:
                            ledButton.getLed().off();
                            display.show("trophy");
                            time.sleep(2);
                            if len(wrongs) > 0:
                                if len(wrongs) > 1:
                                    display.showText(str(len(wrongs)) + " Mistakes");
                                else:
                                    display.showText(str(len(wrongs)) + " Mistake");
                                time.sleep(1);
                            display.clear();
                    return;
            else:
                print("Pressed ", ledButton.name, " (state: ", state, ")")

        red = LedButton("red", 21, 19, callback=popLedOrder);
        green = LedButton("green", 20, 13, callback=popLedOrder);
        blue = LedButton("blue", 16, 6, callback=popLedOrder);
        yellow = LedButton("yellow", 12, 5, callback=popLedOrder);
        ledButtons = [red, green, blue, yellow];

        def blinkLeds(event):
            if event.action == "released":
                for i in range(blinkCount):
                    rnd = random.randint(0, 3);
                    ledButton = ledButtons[rnd];
                    ledOrder.append(ledButton.name);
                    ledButton.getLed().blink(1);
                wrongs.clear();

        sense.stick.direction_middle = blinkLeds;
        while True:
            pass;

    finally:
        print("Finally Goodbye!")


if __name__ == '__main__':
    main(sys.argv[1:])
