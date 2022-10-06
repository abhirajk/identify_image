import numpy as np
import cv2

img = cv2.imread('raspi_utils/data/cutepic.jpg',0);
rows,cols = img.shape;

for i in range(3,11):
    for j in range(3,11):
        k = img[i,j]
        print(k)
