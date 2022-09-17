from .Location import Location


class DetectedFrame:
    targets = [];
    width, height = 0, 0;
    dwidth, dheight = 0, 0;
    image = None;
    processedImage = None;

    def __init__(self, image):
        self.image = image;
        self.dheight = 0
        self.dwidth = 0
        self.height = image.shape[0]
        self.width = image.shape[1]
        self.targets = [];

    def buildLocation(self, detectedBox, paddingSize):
        top, left, bottom, right = detectedBox;
        pwidth = paddingSize[0];
        pheight = paddingSize[1];
        dx = left * self.dwidth;
        dy = top * self.dheight;
        dw = (right * self.dwidth) - dx;
        dh = (bottom * self.dheight) - dy;
        x = (dx * self.width / (self.dwidth - pwidth));
        y = (dy * self.height / (self.dheight - pheight));
        w = (dw * self.width / (self.dwidth - pwidth));
        h = (dh * self.height / (self.dheight - pheight));
        return Location(int(x), int(y), int(w), int(h), int(dx), int(dy), int(dw), int(dh));

    def appendTarget(self, target):
        self.targets.append(target);

    def setProcessedImage(self, processedImage):
        self.processedImage = processedImage;
        self.dheight = processedImage.shape[0]
        self.dwidth = processedImage.shape[1]

    def hasTarget(self, kind, minScore):
        for target in self.targets:
            if target.kind == kind and target.score >= minScore:
                return True;
        return False;

    def __str__(self):
        return "{ width: " + str(self.width) + ", height: " + str(self.height) \
               + ", dwidth: " + str(self.width) + ", dheight: " + str(self.height) \
               + ", targets: [ " + ("".join([str(target) for target in self.targets])) + " ] }";
