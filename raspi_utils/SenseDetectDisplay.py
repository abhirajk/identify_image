import time

import numpy as np
from sense_hat import SenseHat
import cv2
from pathlib import Path

# Define some colours
r = (255, 0, 0)  # Red
g = (0, 255, 0)  # Green
b = (0, 0, 0)  # Black
x = (50, 50, 50)  # Grey

DEFAULT_SHAPE = [
            b, b, b, x, x, b, b, b,
            b, b, x, b, b, x, b, b,
            b, b, x, b, b, x, b, b,
            b, b, b, b, b, x, b, b,
            b, b, b, b, x, b, b, b,
            b, b, b, b, x, b, b, b,
            b, b, b, b, b, b, b, b,
            b, b, b, b, x, b, b, b,
        ];
class SenseDetectDisplay:
    sense = None;
    shapeDictonary = {
        "person": [
            b, b, b, b, b, b, b, b,
            b, b, b, g, g, b, b, b,
            b, b, g, b, b, g, b, b,
            b, b, g, b, b, g, b, b,
            b, b, b, g, g, b, b, b,
            b, b, g, b, b, g, b, b,
            b, g, b, b, b, b, g, b,
            b, g, b, b, b, b, g, b
        ],
        "question": DEFAULT_SHAPE
    };

    @staticmethod
    def loadShapeLabelFile(shapeLabelFilePath: str = None):
        if shapeLabelFilePath is None:
            return None;
        if not Path(shapeLabelFilePath).is_file():
            return None;
        with open(shapeLabelFilePath, 'r') as f:
            lines = f.readlines()
            ret = [];
            for line in lines:
                ret.append(line.strip());
            return ret;
        return None;

    @staticmethod
    def loadShapeFile(shapeFilePath: str, shapeLabels: list[str]):
        if shapeFilePath is None:
            return None;
        if not Path(shapeFilePath).is_file():
            return None;
        shapeImage = cv2.imread(shapeFilePath);
        rows = int(shapeImage.shape[0] / 8);
        cols = int(shapeImage.shape[1] / 8);
        index = 0;
        ishapeDictionary = {};
        for row in range(rows):
            for col in range(cols):
                colorArray = [];
                for i in range(0, 8):
                    for j in range(0, 8):
                        pcolor = shapeImage[i + (8 * row), j + (8 * col)];
                        colorArray.append([pcolor[2], pcolor[1], pcolor[0]]);
                key = index;
                if shapeLabels is not None:
                    key = shapeLabels[index];
                ishapeDictionary[key] = colorArray;
                index = index + 1;
        return ishapeDictionary;

    def __init__(self, sense: SenseHat, shapeFilePath: str = None, shapeLabelFilePath: str = None):
        self.sense = sense;
        sense.set_rotation(90);
        self.sense.low_light = True;
        ishapeDictonary = SenseDetectDisplay.loadShapeFile(shapeFilePath,
                                                           SenseDetectDisplay.loadShapeLabelFile(shapeLabelFilePath));
        if ishapeDictonary is not None:
            self.shapeDictonary = ishapeDictonary;

    def clear(self):
        self.sense.clear();

    def show(self, shape):
        if shape in self.shapeDictonary:
            self.sense.set_pixels(self.shapeDictonary[shape]);
        else:
            self.sense.set_pixels(DEFAULT_SHAPE);

    def showText(self, text):
        self.sense.show_message(text, text_colour = x);

    def showPixel(self, colors, sleep = 0):
        self.sense.clear();
        index = 0;
        if(len(colors)>64):
            return;
        for color in colors:
            row = int(index / 8);
            col = (index % 8)
            self.sense.set_pixel(col, row, color);
            if sleep > 0:
                time.sleep(sleep);
            index = index + 1;
