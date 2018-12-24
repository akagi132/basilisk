#!/usr/bin/env/python
# -*- coding: utf-8 -*-

import cv2
import sys
import numpy as np

TARGET_FILE = 'NULL'

def main(img):
    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('gray.png', image)
    image = cv2.medianBlur(image, 5)
    cv2.imwrite('median.png', image)
    image = cv2.Canny(image, 100, 200)
    cv2.imwrite('canny.png', image)

if __name__ == '__main__':
    if len(sys.argv) < 1:
        print('please set src image')
    else:
        args = sys.argv
        TARGET_FILE = str(args[1])
        target_img = cv2.imread(TARGET_FILE)

        main(target_img)

