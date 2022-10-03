from sense_hat import SenseHat

# Define some colours
r = (255, 0, 0) # Red
g = (0, 255, 0) # Green
b = (0, 0, 0) # Black
x = (50, 50, 50) # Grey

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
    "question": [
                b, b, b, x, x, b, b, b,
                b, b, x, b, b, x, b, b,
                b, b, x, b, b, x, b, b,
                b, b, b, b, b, x, b, b,
                b, b, b, b, x, b, b, b,
                b, b, b, b, x, b, b, b,
                b, b, b, b, b, b, b, b,
                b, b, b, b, x, b, b, b,
            ]
};

class SenseDetectDisplay:

    sense = None;

    def __init__(self):
        self.sense = SenseHat()
        self.sense.low_light = True;

    def clear(self):
        self.sense.clear();

    def show(self, shape):
        self.sense.set_pixels(shapeDictonary[shape]);