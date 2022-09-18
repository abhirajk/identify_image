from picamera.array import PiRGBArray
from picamera import PiCamera
import time

from raspi_utils.ColorLed import ColorLed

from image_recognition.DetectionEngine import DetectionEngine

import signal
import sys

# Setup LED
colorLed = ColorLed(17, 27, 22);


def sigint_handler(sig, frame):
    print('KeyboardInterrupt is caught');
    colorLed.off();
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)


def main():
    detectionEngine = DetectionEngine("/home/pi/identify_image/models/picam-example/mobilenet_v2.tflite",
                                      "/home/pi/identify_image/models/picam-example/labels/coco_labels.txt")

    # Setup camera
    camera = PiCamera()
    camera.exposure_mode = "sports";
    camera.iso = 800;
    camera.resolution = (640, 480);
    camera.vflip = True;
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
            colorLed.color("green");
            noPersonFoundCount = 0;
            if (personFoundCount < 5):
                personFoundCount += 1;
            time.sleep(personFoundCount / 10);
        else:
            colorLed.color("red");
            personFoundCount = 0;
            if (noPersonFoundCount < 5):
                noPersonFoundCount += 1;
            time.sleep(noPersonFoundCount / 10);


if __name__ == '__main__':
    main()
