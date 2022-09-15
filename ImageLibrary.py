import cv2

from Frame import Frame


def drawDetectedImage(frame: Frame):
    imageCopy = frame.processedImage.copy();
    for target in frame.targets:
        rect_start = (int(target.location.dx), int(target.location.dy))
        rect_end = (int(target.location.dx + target.location.dwidth), int(target.location.dy + target.location.dheight))
        print(rect_start, rect_end);
        cv2.rectangle(imageCopy, rect_start, rect_end, (0, 255, 0, 0))
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(imageCopy, target.kind, (int(target.location.dx) + 10, int(target.location.dy) + 10), font, 1, (0, 0, 255), 2, cv2.LINE_AA);
    return imageCopy;