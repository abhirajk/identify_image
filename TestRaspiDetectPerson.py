from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from sense_hat import SenseHat

from raspi_utils.ColorLed import ColorLed

from image_recognition.DetectionEngine import DetectionEngine

import signal
import sys

# Setup LED
# colorLed = ColorLed(17, 27, 22);

# Define some colours
r = (255, 0, 0) # Red
g = (0, 255, 0) # Green
b = (0, 0, 0) # Black

# Set up where each colour will display
person = [
    b, b, b, b, b, b, b, b,
    b, b, b, g, g, b, b, b,
    b, b, g, b, b, g, b, b,
    b, b, g, b, b, g, b, b,
    b, b, b, g, g, b, b, b,
    b, b, g, b, b, g, b, b,
    b, g, b, b, b, b, g, b,
    b, g, b, b, b, b, g, b
]
noperson = [
    b, b, r, r, r, r, b, b,
    b, r, b, g, g, b, r, b,
    r, b, g, b, b, r, b, r,
    r, b, g, b, r, g, b, r,
    r, b, b, r, g, b, b, r,
    r, b, r, b, b, g, b, r,
    b, r, b, b, b, b, r, b,
    b, g, r, r, r, r, g, b
]
sense = SenseHat()
sense.low_light = True;


def sigint_handler(sig, frame):
    print('KeyboardInterrupt is caught');
    sense.clear();
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)


def main(args: list[str]) -> None:
    #detectionEngine = DetectionEngine("/home/pi/identify_image/models/picam-example/mobilenet_v2.tflite",
    #                                  "/home/pi/identify_image/models/picam-example/labels/coco_labels.txt")
    if len(args) < 2:
        print("Required parameter model file & labels file missing");
        exit(1);

    detectionEngine = DetectionEngine(args[0], args[1]);

    # Setup camera
    camera = PiCamera()
    camera.exposure_mode = "sports";
    camera.iso = 800;
    camera.resolution = (640, 480);
    rawCapture = PiRGBArray(camera);
    # allow the camera to warmup
    time.sleep(0.1)

    noPersonFoundCount = 0;
    personFoundCount = 0;
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        rawCapture.truncate()
        rawCapture.seek(0)
        start = time.process_time_ns();
        detectedFrame = detectionEngine.detect(frame.array);
        end = time.process_time_ns();
        print("TimeTaken: ", str((end - start) / 1000000), "ms", " Person: ", detectedFrame.hasTarget("person", 0.7));

        if detectedFrame.hasTarget("person", 0.7):
            sense.set_pixels(person);
            noPersonFoundCount = 0;
            if (personFoundCount < 5):
                personFoundCount += 1;
            time.sleep(personFoundCount / 10);
        else:
            sense.set_pixels(noperson);
            personFoundCount = 0;
            if (noPersonFoundCount < 5):
                noPersonFoundCount += 1;
            time.sleep(noPersonFoundCount / 10);


if __name__ == '__main__':
    main(sys.argv[1:])
