import random
import time
from queue import Queue

import RPi.GPIO as GPIO
from raspi_utils.LedButton import LedButton
from sense_hat import SenseHat

from raspi_utils.SenseDetectDisplay import SenseDetectDisplay
import signal
import sys

red = (255, 0, 0);
grey = (50, 50, 50);
green = (0, 255, 0);
yellow = (255, 255, 0);

sense = SenseHat();
display = SenseDetectDisplay(sense, shapeFilePath="raspi_utils/data/game.png"
                             , shapeLabelFilePath="raspi_utils/data/game.txt");


class Game:
    start = 0;
    blinkCount = 4;
    ledOrder = [];
    wrongs = [];
    status = [];

    def __init__(self):
        red = LedButton("red", ledPin=26, buttonPin=21, callback=self.popLedOrder);
        green = LedButton("green", ledPin=19, buttonPin=20, callback=self.popLedOrder);
        blue = LedButton("blue", ledPin=13, buttonPin=16, callback=self.popLedOrder);
        yellow = LedButton("yellow", ledPin=6, buttonPin=12, callback=self.popLedOrder);
        self.ledButtons = [red, green, blue, yellow];

    def popLedOrder(self, ledButton, state):
        if len(self.ledOrder) > 0 and self.start == 1:
            if state == "on":
                expected = self.ledOrder[0];
                if expected != ledButton.name:
                    self.status[self.blinkCount - len(self.ledOrder)] = -1;
                    self.wrongs.append(len(self.ledOrder));
                    self.showDots();
                else:
                    if self.status[self.blinkCount - len(self.ledOrder)] == 0:
                        self.status[self.blinkCount - len(self.ledOrder)] = 1;
                    else:
                        self.status[self.blinkCount - len(self.ledOrder)] = -2;
                    del self.ledOrder[0];
                    self.showDots();
                    if len(self.ledOrder) == 0:
                        ledButton.getLed().off();
                        time.sleep(1);
                        if len(self.wrongs) <= 0:
                            display.show("trophy");
                            time.sleep(1);
                            self.blinkCount = self.blinkCount + 1;
                            self.startGame();
                        else:
                            display.show("trophy");
                            time.sleep(2);
                            self.showDots();
                            time.sleep(2);
                            display.clear();
                return;
        else:
            print(ledButton.name);

    def resetGame(self):
        self.blinkCount = 4;

    def startGame(self):
        self.start = 0;
        self.ledOrder = [];
        self.buildDots();
        time.sleep(2);
        for i in range(self.blinkCount):
            rnd = random.randint(0, 3);
            ledButton = self.ledButtons[rnd];
            self.ledOrder.append(ledButton.name);
            ledButton.getLed().blink(1);
        print(self.ledOrder);
        self.wrongs.clear();
        self.start = 1;

    def showDots(self, withSleep=False):
        colors = [];
        for i in range(len(self.status)):
            color = grey;
            if self.status[i] == 1:
                color = green;
            elif self.status[i] == -1:
                color = red;
            elif self.status[i] == -2:
                color = yellow;
            colors.append(color);
        sleep = 0;
        if withSleep:
            sleep = 0.3
        display.showPixel(colors, sleep);
        if withSleep:
            time.sleep(2);

    def increment(self):
        self.blinkCount = self.blinkCount + 1;
        self.buildDots();

    def decrement(self):
        self.blinkCount = self.blinkCount - 1;
        if(self.blinkCount<=0):
            self.blinkCount = 1;
        self.buildDots();

    def buildDots(self):
        self.status = [];
        for i in range(self.blinkCount):
            self.status.append(0);
        self.showDots(False);



def sigint_handler(sig, frame):
    display.clear();
    GPIO.cleanup();
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)


def main(args: list[str]) -> None:
    try:
        print("Lets Play memory game")
        game = Game();

        def blinkLeds(event):
            if event.action == "released":
                game.startGame();

        def incrementBlinkCount(event):
            if event.action == "released":
                game.increment();

        def decrementBlinkCount(event):
            if event.action == "released":
                game.decrement();

        sense.stick.direction_middle = blinkLeds;
        sense.stick.direction_up = incrementBlinkCount;
        sense.stick.direction_right = incrementBlinkCount;
        sense.stick.direction_down = decrementBlinkCount;
        sense.stick.direction_left = decrementBlinkCount;
        while True:
            pass;
    finally:
        print("Finally Goodbye!")


if __name__ == '__main__':
    main(sys.argv[1:])
