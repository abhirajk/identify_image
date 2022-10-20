from .DetectedFrame import DetectedFrame


class TargetShift:
    xcenter, ycenter, xshift, yshift, xperc, yperc, targetWidth, targetHeight, frameWidth, frameHeight = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0;

    def __init__(self, xcenter: int, ycenter: int,
                 xshift: int, yshift: int,
                 xperc: int, yperc: int,
                 targetWidth: int, targetHeight: int,
                 frameWidth: int, frameHeight: int):
        self.xcenter = xcenter;
        self.ycenter = ycenter;
        self.xshift = xshift;
        self.yshift = yshift;
        self.xperc = xperc;
        self.yperc = yperc;
        self.targetWidth = targetWidth;
        self.targetHeight = targetHeight;
        self.frameWidth = frameWidth;
        self.frameHeight = frameHeight;

    def __str__(self):
        return "{ xs: " + str(self.xshift) + "("+str(self.xperc)+"%), ys: " + str(self.yshift) + "("+str(self.yperc)+"%)" \
               + ", xc: " + str(self.xcenter) + "("+str(self.frameWidth/2)+")" + ", yc: " + str(self.ycenter) +"("+ str(self.frameHeight/2) +")"\
               + ", w: " + str(self.targetWidth) + "("+str(self.frameWidth)+")" + ", h: " + str(self.targetHeight) + "("+ str(self.frameHeight) +") }";


def computeCenterShift(frame: DetectedFrame, kind: str) -> TargetShift:
    if len(frame.targets) == 0 or len(frame.targets) > 1:
        print("More targets");
    target = frame.getTarget(kind, 0);
    if target is not None:
        centerPoint = target.location.centerPoint();
        targetWidth = target.location.width;
        targetHeight = target.location.height;
        width = frame.width;
        height = frame.height;
        xcenter = centerPoint[0];
        ycenter = centerPoint[1];
        xshift = int((width / 2) - xcenter);
        yshift = int((height / 2) - ycenter);
        xperc = int(xshift * 100 / width);
        yperc = int(yshift * 100 / height);
        return TargetShift(xcenter, ycenter, xshift, yshift, xperc, yperc, targetWidth, targetHeight, width, height);
    return None;