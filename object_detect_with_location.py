import argparse
import os
import sys

import cv2
import numpy as np
import tflite_runtime.interpreter as tflite
from PIL import Image, ImageDraw, ImageFont

normalSize = (640, 480)
lowresSize = (320, 240)

rectangles = []

def ReadLabelFileNoIndex(filename):
  with open(filename, 'r') as f:
    return [line.strip() for line in f.readlines()]

def ReadLabelFile(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    ret = {}
    for line in lines:
        pair = line.strip().split(maxsplit=1)
        ret[int(pair[0])] = pair[1].strip()
    return ret

def DrawRectangles(image, rectangles):
    for rect in rectangles:
        print(rect)
        rect_start = (int(rect[0]), int(rect[1]))
        rect_end = (int(rect[2]), int(rect[3]))
        print("Start rectangle - ", rect_start);
        print("End rectangle - ", rect_end);
        cv2.rectangle(image, rect_start, rect_end, (0, 255, 0, 0))
        if len(rect) == 5:
            text = rect[4]
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(image, text, (int(rect[0] * 2) + 10, int(rect[1] * 2) + 10), font, 1, (0, 0, 255), 2, cv2.LINE_AA)

def InferenceTensorFlow(image, model, label=None):
    if label:
        labels = ReadLabelFile(label)
    else:
        labels = None

    interpreter = tflite.Interpreter(model_path=model, num_threads=4)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]
    floating_model = False
    if input_details[0]['dtype'] == np.float32:
        floating_model = True

    oheight, owidth, channels = image.shape;
    if (height / width) != (oheight / owidth):
        rheight = height;
        rwidth = width;
        top = 0;
        left = 0;
        bottom = 0;
        right = 0;
        if oheight>owidth:
            rwidth = int((rheight / oheight) * owidth);
            right = width - rwidth;
        else:
            rheight = int((rwidth / owidth) * oheight);
            bottom = height - rheight;
        print("Resize to Width: ", rwidth, " Height: ", rheight);
        picture = cv2.resize(image, (rwidth, rheight));
        picture = cv2.copyMakeBorder(picture, top, bottom, left, right, cv2.BORDER_CONSTANT, 0)
    else:
        picture = cv2.resize(image, (width, height));

    print('Resize Dimension    : ', picture.shape);
    cv2.imwrite("/home/pi/identify_image/testresized.jpg", picture);
    input_data = np.expand_dims(picture, axis=0)
    if floating_model:
        input_data = (np.float32(input_data) - 127.5) / 127.5

    interpreter.set_tensor(input_details[0]['index'], input_data)

    interpreter.invoke()

    detected_boxes = interpreter.get_tensor(output_details[0]['index'])
    detected_classes = interpreter.get_tensor(output_details[1]['index'])
    detected_scores = interpreter.get_tensor(output_details[2]['index'])
    num_boxes = interpreter.get_tensor(output_details[3]['index'])

    rectangles = []
    for i in range(int(num_boxes)):
        top, left, bottom, right = detected_boxes[0][i]
        classId = int(detected_classes[0][i])
        score = detected_scores[0][i]
        if score > 0.5:
            print(detected_boxes[0][i]);
            xmin = left * width;
            ymin = top * height;
            xmax = right * width;
            ymax = bottom * height;
            box = [xmin, ymin, xmax, ymax];
            print("Box: ", box);
            rectangles.append(box)
            if labels:
                print(labels[classId], 'score = ', score)
                rectangles[-1].append(labels[classId])
            else:
                print('score = ', score)

    print("Done Generating output image");
    DrawRectangles(picture, rectangles);
    cv2.imwrite("/home/pi/identify_image/testout.jpg", picture);
    print("After saving image:")
    print(os.listdir("/home/pi/identify_image/"))

    print('Successfully saved')


def main():
    img = cv2.imread("/home/pi/identify_image/testperson_1.jpg", cv2.IMREAD_UNCHANGED)

    # get dimensions of image
    dimensions = img.shape

    # height, width, number of channels in image
    height = img.shape[0]
    width = img.shape[1]
    channels = img.shape[2]

    print('Image Dimension    : ', dimensions)
    print('Image Height       : ', height)
    print('Image Width        : ', width)
    print('Number of Channels : ', channels)


    InferenceTensorFlow(img, "/home/pi/identify_image/models/picam-example/mobilenet_v2.tflite", "/home/pi/identify_image/models/picam-example/labels/coco_labels.txt");

    #InferenceTensorFlow(img, "/home/pi/identify_image/models/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29/detect.tflite", "/home/pi/identify_image/models/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29/labelmap.txt");

    #InferenceTensorFlow(img, "/home/pi/identify_image/models/testcoco/detect.tflite", "/home/pi/identify_image/models/testcoco/labelmap.txt");

if __name__ == '__main__':
    main()
