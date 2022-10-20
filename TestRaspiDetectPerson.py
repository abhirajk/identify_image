from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from sense_hat import SenseHat
import threading
import logging


from image_recognition.ImageUtils import drawDetectedImage
from image_recognition.TargetShift import TargetShift, computeCenterShift
from raspi_utils.CameraPlatform import CameraPlatform
from raspi_utils.SenseDetectDisplay import SenseDetectDisplay
from raspi_utils.ColorLed import ColorLed
from image_recognition.DetectionEngine import DetectionEngine

import signal
import sys

# Setup LED
# colorLed = ColorLed(17, 27, 22);
# Display object on sense hat
print("Creating SenseDetectDisplay...")
sense = SenseHat();
display = SenseDetectDisplay(sense, shapeFilePath = "raspi_utils/data/detect_person.png"
                             , shapeLabelFilePath = "raspi_utils/data/detect_person.txt");
print("Created SenseDetectDisplay");

print("Creating CameraPlatform...")
cameraPlatform = CameraPlatform();
print("Created CameraPlatform...")


def scanCamera(cameraPlatform: CameraPlatform = None):
    logging.info("Starting camera platform scan");
    while True:
        cameraPlatform.scanXPlane();
        logging.info("Sleeping before next sweep");
        time.sleep(0.5);
    logging.info("Stoping camera platform scan");

def sigint_handler(sig, frame):
    print('KeyboardInterrupt is caught');
    display.clear();
    cameraPlatform.clean();
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)


def main(args: list[str]) -> None:
    if len(args) < 2:
        print("Required parameter model file & labels file missing");
        exit(1);

    print("Creating DetectionEngine...")
    detectionEngine = DetectionEngine(args[0], args[1]);
    print("Created DetectionEngine")

    x = threading.Thread(target=scanCamera, args=(cameraPlatform,), daemon=True);
    x.start();

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
    print("Start sensing...");
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        rawCapture.truncate()
        rawCapture.seek(0)
        start = time.process_time_ns();
        detectedFrame = detectionEngine.detect(frame.array);
        end = time.process_time_ns();
        cv2.imshow('image', drawDetectedImage(detectedFrame));
        cv2.waitKey(2);
        targetShift = computeCenterShift(detectedFrame, "person");
        #cv2.imwrite("savedImage.jpeg", drawDetectedImage(detectedFrame));
        print("TimeTaken: ", str((end - start) / 1000000), "ms - "
              , detectedFrame.hasTarget("person", 0.7), " < "
              , detectedFrame.hasTarget("person", 0.5));
        if detectedFrame.hasTarget("person", 0.5):
            display.show("person");
            noPersonFoundCount = 0;
            if (personFoundCount < 5):
                personFoundCount += 1;
            xshift = 0;
            yshift = 0;
            if targetShift is not None:
                xshift = int(targetShift.xshift / 10);
                yshift = int(-1 * targetShift.yshift / 20);
                print("Shift >>>> x: ", xshift, " / y: ", yshift);
            else:
                print("Shift <><> ", 0);
            cameraPlatform.shiftXPlane(xshift);
            cameraPlatform.shiftYPlane(yshift);
            time.sleep(personFoundCount / 10);
        else:
            display.show("noperson");
            personFoundCount = 0;
            if (noPersonFoundCount < 5):
                noPersonFoundCount += 1;
            cameraPlatform.sweepXPlane = True;
            time.sleep(noPersonFoundCount / 10);


if __name__ == '__main__':
    main(sys.argv[1:])
