#!/bin/env/pyton3
import cv2
import sys

src = 'NULL'
comp = 'NULL'

def main():
    src_img = cv2.imread(src)
    cmp_img = cv2.imread(comp)
    res = cv2.matchTemplate(src_img, cmp_img, cv2.TM_SQDIFF)
    print(res)

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print('please set src image, compare image.')
    else:
        src = sys.argv[1]
        comp = sys.argv[2]
        main()
