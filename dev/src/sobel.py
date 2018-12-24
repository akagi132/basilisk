#!/usr/bin/env/python
# -*- coding: utf-8 -*-

import cv2
import sys
import numpy as np

TARGET_FILE = 'NULL'

def main(img):
    dx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    dy = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
    image = np.sqrt(dx ** 2 + dy ** 2)
    cv2.imwrite('sobel.png', image)

if __name__ == '__main__':
    if len(sys.argv) < 1:
        print('please set src image')
    else:
        args = sys.argv
        TARGET_FILE = str(args[1])
        target_img = cv2.imread(TARGET_FILE)

        main(target_img)

