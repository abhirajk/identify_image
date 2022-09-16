import cv2

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from fractions import Fraction

import ImageLibrary
from TargetShift import TargetShift

from DetectionEngine import DetectionEngine
from Frame import Frame

import RPi.GPIO as GPIO;

import signal
import sys

def sigint_handler(signal, frame):
    print ('KeyboardInterrupt is caught');
    GPIO.output(21, GPIO.LOW);
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

def main():
    detectionEngine = DetectionEngine("/home/pi/identify_image/models/picam-example/mobilenet_v2.tflite", "/home/pi/identify_image/models/picam-example/labels/coco_labels.txt")

    # Force sensor mode 3 (the long exposure mode), set
    # the framerate to 1/6fps, the shutter speed to 6s,
    # and ISO to 800 (for maximum gain)
    camera = PiCamera()
    camera.exposure_mode = "sports";
    camera.iso = 800;
    camera.resolution = (640, 480);
    camera.vflip = True;
    rawCapture = PiRGBArray(camera);
    # allow the camera to warmup
    time.sleep(0.1)

    GPIO.setmode(GPIO.BCM);
    GPIO.setwarnings(False);
    GPIO.setup(21, GPIO.OUT);

    noPersonFoundCount = 0;
    personFoundCount = 0;
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        rawCapture.truncate()
        rawCapture.seek(0)
        start = time.process_time_ns();
        detectedFrame = detectionEngine.detect(frame.array);
        end = time.process_time_ns();
        print("TimeTaken: ", str((end - start)/1000000), "ms", " Frame: ", detectedFrame);
        if(detectedFrame.hasTarget("person")):
            GPIO.output(21, GPIO.HIGH);
            noPersonFoundCount = 0;
            if (personFoundCount < 5):
                personFoundCount += 1;
            time.sleep(personFoundCount/10);
        else:
            GPIO.output(21, GPIO.LOW);
            personFoundCount = 0;
            if (noPersonFoundCount < 5):
                noPersonFoundCount += 1;
            time.sleep(noPersonFoundCount/10);

if __name__ == '__main__':
    main()