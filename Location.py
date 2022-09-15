class Location:
    def __init__(self, x: int, y: int, w: int, h: int, dx: int, dy: int, dw: int, dh: int):
        self.x = x;
        self.y = y;
        self.width = w;
        self.height = h;
        self.dx = dx;
        self.dy = dy;
        self.dwidth = dw;
        self.dheight = dh;

    def centerPoint(self):
        return tuple((int((self.x + self.width) / 2), int((self.y + self.height) / 2)))

    def __str__(self):
        return "{ x: " + str(self.x) +", y: " + str(self.y) +", width: " + str(self.width) + ", height: " + str(self.height) \
               + ", dx: " + str(self.dx) +", dy: " + str(self.dy) +", dwidth: " + str(self.dwidth) + ", dheight: " + str(self.dheight) + "  }";