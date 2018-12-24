#!/usr/bin/env/python
# -*- coding: utf-8 -*-

import cv2
import sys

def main(target_img, compare_img):
    IMG_SIZE = (200, 200)

    target_img = cv2.resize(target_img, IMG_SIZE)
    target_hist = cv2.calcHist([target_img], [0], None, [256], [0, 256])

    compare_img = cv2.resize(compare_img, IMG_SIZE)
    compare_hist = cv2.calcHist([compare_img], [0], None, [256], [0, 256])

    ret = cv2.compareHist(target_hist, compare_hist, 0)
    print(ret)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('please set src image and compare image')
    else:
        args = sys.argv
        TARGET_FILE = str(args[1])
        COMPARE_FILE = str(args[2])
        target_img = cv2.imread(TARGET_FILE)
        compare_img = cv2.imread(COMPARE_FILE)

        main(target_img, compare_img)
