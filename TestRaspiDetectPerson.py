from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

from image_recognition.ImageUtils import drawDetectedImage
from image_recognition.TargetShift import TargetShift, computeCenterShift
from raspi_utils.SenseDetectDisplay import SenseDetectDisplay
from raspi_utils.ColorLed import ColorLed
from image_recognition.DetectionEngine import DetectionEngine

import signal
import sys

# Setup LED
# colorLed = ColorLed(17, 27, 22);
# Display object on sense hat
display = SenseDetectDisplay();

def sigint_handler(sig, frame):
    print('KeyboardInterrupt is caught');
    display.clear();
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)


def main(args: list[str]) -> None:
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
        targetShift = computeCenterShift(detectedFrame, "person");
        #cv2.imwrite("savedImage.jpeg", drawDetectedImage(detectedFrame));
        print("TimeTaken: ", str((end - start) / 1000000), "ms - ", str(targetShift));
        if detectedFrame.hasTarget("person", 0.7):
            display.show("person");
            noPersonFoundCount = 0;
            if (personFoundCount < 5):
                personFoundCount += 1;
            time.sleep(personFoundCount / 10);
        else:
            display.show("question");
            personFoundCount = 0;
            if (noPersonFoundCount < 5):
                noPersonFoundCount += 1;
            time.sleep(noPersonFoundCount / 10);


if __name__ == '__main__':
    main(sys.argv[1:])
