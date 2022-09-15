import cv2

import ImageLibrary

from DetectionEngine import DetectionEngine
from Frame import Frame


def main():
    img = cv2.imread("/home/pi/identify_image/testperson_1.jpg", cv2.IMREAD_UNCHANGED)
    detectionEngine = DetectionEngine("/home/pi/identify_image/models/picam-example/mobilenet_v2.tflite", "/home/pi/identify_image/models/picam-example/labels/coco_labels.txt")
    frame = detectionEngine.detect(img);
    print(frame);
    print(frame.hasTarget())
    print(frame.getCenterShift());
    cv2.imwrite("/home/pi/identify_image/testperson_1_dout.jpg", ImageLibrary.drawDetectedImage(frame));
    cv2.imwrite("/home/pi/identify_image/testperson_1_out.jpg", ImageLibrary.drawOriginalImage(frame));

if __name__ == '__main__':
    main()