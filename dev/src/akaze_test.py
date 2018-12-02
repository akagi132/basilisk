#!/usr/bin/env/python
# -*- coding: utf-8 -*-

import cv2
import sys

TARGET_FILE = 'NULL'
COMPARE_FILE = 'NULL'

def main():
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    detector = cv2.AKAZE_create()
    (target_kp, target_des) = calc_kp_and_des(TARGET_FILE, detector)
    
    try:
        (comparing_kp, comparing_des) = calc_kp_and_des(COMPARE_FILE, detector)
        matches = bf.match(target_des, comparing_des)
        dist = [m.distance for m in matches]
        ret = sum(dist) / len(dist)
    except cv2.error:
        ret = 100000

    print(ret)

def calc_kp_and_des(img_path, detector):
    """
        特徴点と識別子を計算する
        :param str img_path: イメージのディレクトリパス
        :param detector: 算出のアルゴリズム
        :return: keypoints　　特徴点？
        :return: descriptor　特徴量？
    """
    IMG_SIZE = (500, 500)
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, IMG_SIZE)
    return detector.detectAndCompute(img, None)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('please set src image and compare image')
    else:
        args = sys.argv
        TARGET_FILE = str(args[1])
        COMPARE_FILE = str(args[2])
        main()

