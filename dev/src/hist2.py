#!/usr/bin/env/python
# -*- coding: utf-8 -*-

import cv2
import sys
import numpy as np

THRESHOLD = 0

def main(img, img2):
    width = int(img.shape[1] * 0.3)
    height = int(img.shape[0] * 0.3)

    target_img = cv2.resize(img, (width, height))
    target_img = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('target_img.png', target_img)

    compare_img = cv2.resize(img2, (width, height))
    compare_img = cv2.cvtColor(compare_img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('compare_img.png', compare_img)

    dist_img = cv2.resize(img, (width, height))
    sim = 0

    for i in range(height):
        for j in range(width):
            sub = abs(int(target_img[i, j]) - int(compare_img[i, j]))
            if (sub > THRESHOLD):
                sim += 1
                dist_img[i, j] = [0, sub, 0]
            else:
                gray = target_img[i, j]
                dist_img[i, j] = [gray, gray, gray]

    print(sim)
    cv2.imwrite('dist.png', dist_img)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('please set src image and compare image')
    else:
        args = sys.argv
        TARGET_FILE = str(args[1])
        COMPARE_FILE = str(args[2])
        THRESHOLD = int(args[3])
        target_img = cv2.imread(TARGET_FILE)
        compare_img = cv2.imread(COMPARE_FILE)

        main(target_img, compare_img)
