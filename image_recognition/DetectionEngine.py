import cv2
import numpy as np

import tflite_runtime.interpreter as tflite

from .DetectedFrame import DetectedFrame
from .Target import Target


class DetectionEngine:
    labels = None;
    height = 0;
    width = 0;
    floatingModel = False;
    interpreter = None;
    index = None;

    @staticmethod
    def ReadLabelFile(labelFile):
        with open(labelFile, 'r') as f:
            lines = f.readlines()
        ret = {}
        for line in lines:
            pair = line.strip().split(maxsplit=1)
            ret[int(pair[0])] = pair[1].strip()
        return ret

    def __init__(self, modelFile, labelFile):
        if labelFile:
            self.labels = DetectionEngine.ReadLabelFile(labelFile)
        else:
            self.labels = None

        self.interpreter = tflite.Interpreter(model_path=modelFile, num_threads=4)
        self.interpreter.allocate_tensors()

        input_details = self.interpreter.get_input_details()
        self.height = input_details[0]['shape'][1]
        self.width = input_details[0]['shape'][2]
        self.index = input_details[0]['index'];
        self.floatingModel = False
        if input_details[0]['dtype'] == np.float32:
            self.floatingModel = True

    def detect(self, image):
        frame = DetectedFrame(image);
        oheight, owidth, channels = frame.image.shape;
        paddingSize = (0, 0);
        if (self.height / self.width) != (oheight / owidth):
            rheight = self.height;
            rwidth = self.width;
            top = 0;
            left = 0;
            bottom = 0;
            right = 0;
            if oheight > owidth:
                rwidth = int((rheight / oheight) * owidth);
                right = self.width - rwidth;
            else:
                rheight = int((rwidth / owidth) * oheight);
                bottom = self.height - rheight;
            picture = cv2.resize(frame.image, (rwidth, rheight));
            paddingSize = (right, bottom);
            picture = cv2.copyMakeBorder(picture, top, bottom, left, right, cv2.BORDER_CONSTANT, 0)
        else:
            picture = cv2.resize(frame.image, (self.width, self.height));

        frame.setProcessedImage(picture);
        input_data = np.expand_dims(picture, axis=0)
        if self.floatingModel:
            input_data = (np.float32(input_data) - 127.5) / 127.5

        self.interpreter.set_tensor(self.index, input_data)

        self.interpreter.invoke()

        output_details = self.interpreter.get_output_details()
        detected_boxes = self.interpreter.get_tensor(output_details[0]['index'])
        detected_classes = self.interpreter.get_tensor(output_details[1]['index'])
        detected_scores = self.interpreter.get_tensor(output_details[2]['index'])
        num_boxes = self.interpreter.get_tensor(output_details[3]['index'])

        for i in range(int(num_boxes)):
            score = detected_scores[0][i]
            if score > 0.5:
                location = frame.buildLocation(detected_boxes[0][i], paddingSize)
                classId = int(detected_classes[0][i])
                type = self.labels[classId]
                frame.appendTarget(Target(type, score, location))

        return frame
