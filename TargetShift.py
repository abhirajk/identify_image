from Frame import Frame


class TargetShift:
    xcenter, ycenter, xshift, yshift, xperc, yperc, targetWidth, targetHeight = 0, 0, 0, 0, 0, 0, 0, 0;

    def __init__(self, xcenter: int, ycenter: int, xshift: int, yshift: int, xperc: int, yperc: int, targetWidth: int, targetHeight: int):
        self.xcenter = xcenter;
        self.ycenter = ycenter;
        self.xshift = xshift;
        self.yshift = yshift;
        self.xperc = xperc;
        self.yperc = yperc;
        self.targetWidth = targetWidth;
        self.targetHeight = targetHeight;

    def __str__(self):
        return "{ xperc: " + str(self.xperc) + ", yperc: " + str(self.yperc) \
               + ", xcenter: " + str(self.xcenter) + ", ycenter: " + str(self.ycenter) \
               + ", xshift: " + str(self.xshift) + ", yshift: " + str(self.yshift) \
               + ", width: " + str(self.targetWidth) + ", height: " + str(self.targetHeight) + " }";

    @staticmethod
    def computeCenterShift(frame: Frame):
        if len(frame.targets) == 0 or len(frame.targets) > 1:
            return None;
        else:
            centerPoint = frame.targets[0].location.centerPoint();
            targetWidth = frame.targets[0].location.width;
            targetHeight = frame.targets[0].location.height;
            width = frame.width;
            height = frame.height;
            xcenter = centerPoint[0];
            ycenter = centerPoint[1];
            xshift = int((targetWidth / 2) - xcenter);
            yshift = int((targetHeight / 2) - ycenter);
            xperc = int(xshift * 100 / width);
            yperc = int(yshift * 100 / height);
            return TargetShift(xcenter, ycenter, xshift, yshift, xperc, yperc, targetWidth, targetHeight);