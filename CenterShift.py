from Frame import Frame


class CenterShift:
    xcenter, ycenter, xshift, yshift, xperc, yperc, width, height = 0, 0, 0, 0, 0, 0, 0, 0;

    def __init__(self, centerPoint, targetWidth: int, targetHeight: int, width: int, height: int):
        self.xcenter = centerPoint[0];
        self.ycenter = centerPoint[1];
        self.xshift = int((targetWidth / 2) - self.xcenter);
        self.yshift = int((targetHeight / 2) - self.ycenter);
        self.xperc = int(self.xshift * 100 / width);
        self.yperc = int(self.yshift * 100 / height);
        self.width = targetWidth;
        self.height = targetHeight;

    def __str__(self):
        return "{ xperc: " + str(self.xperc) + ", yperc: " + str(self.yperc) \
               + ", xcenter: " + str(self.xcenter) + ", ycenter: " + str(self.ycenter) \
               + ", xshift: " + str(self.xshift) + ", yshift: " + str(self.yshift) \
               + ", width: " + str(self.width) + ", height: " + str(self.height) + " }";

    @staticmethod
    def computeCenterShift(frame: Frame):
        if len(frame.targets) == 0 or len(frame.targets) > 1:
            return None;
        else:
            return CenterShift(frame.targets[0].location.centerPoint(), frame.targets[0].location.width, frame.targets[0].location.height, frame.width, frame.height);