class CenterShift:
    xperc, yperc, width, height = 0, 0, 0, 0;

    def __init__(self, centerPoint, width: int, height: int):
        print(centerPoint);
        self.xperc = int(((width / 2) - centerPoint[0]) * 100 / width);
        self.yperc = int(((height / 2) - centerPoint[1]) * 100 / height);
        self.width = width;
        self.height = height;

    def __str__(self):
        return "{ xperc: " + str(self.xperc) + ", yperc: " + str(self.yperc) \
               + ", xpixel: " + str(int(self.xperc * self.width / 100)) + ", ypixel: " + str(int(self.yperc * self.height / 100)) \
               + ", width: " + str(self.width) + ", height: " + str(self.height) + " }";
