#!/usr/bin/env/python
# -*- coding: utf-8 -*-

import cv2
import sys

TARGET_FILE = 'NULL'
COMPARE_FILE = 'NULL'

def main(target_img, compare_img):
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    detector = cv2.AKAZE_create()
    (target_kp, target_des) = calc_kp_and_des(target_img, detector)
    (compare_kp, compare_des) = calc_kp_and_des(compare_img, detector)

    matches = bf.knnMatch(target_des, compare_des, k=2)

    ratio = 40
    dist = []
    good = []
    for m, n in matches:
        if m.distance < ratio * n.distance:
            good.append([m])
            dist.append(m.distance)

    ret = sum(dist) / len(dist)
    print(ret)
    image = cv2.drawMatchesKnn(target_img, target_kp, compare_img, compare_kp, good, None, flags=2)
    cv2.imwrite('compare.png', image)

def calc_kp_and_des(img_src, detector):
    """
        特徴点と識別子を計算する
        :param str img_path: イメージのディレクトリパス
        :param detector: 算出のアルゴリズム
        :return: keypoints　　特徴点？
        :return: descriptor　特徴量？
    """
    IMG_SIZE = (500, 500)
    img_gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.resize(img_gray, IMG_SIZE)
    return detector.detectAndCompute(img_gray, None)

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

