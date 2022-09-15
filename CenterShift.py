class CenterShift:
    xcenter, ycenter, xshift, yshift, xperc, yperc, width, height = 0, 0, 0, 0, 0, 0, 0, 0;

    def __init__(self, centerPoint, targetWidth: int, targetHeight: int, width: int, height: int):
        print(centerPoint);
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
