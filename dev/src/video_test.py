#!/bin/env/python3

import cv2
import threading
file_name = '/home/fokko/snake_system/dev/include/video/snake_dinner.mp4'

def read_video(src):
    video = []
    cap = cv2.VideoCapture(src)

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    print('FRAME_COUNT:', frame_count)
    print('FPS:', fps)

#    while (cap.isOpened()):
    count = 0
    shift = 0
    while (count <= 60):
        print(count)
        cap.set(cv2.CAP_PROP_POS_FRAMES, shift * 30)
        ret, frame = cap.read()
        if ret:
            video.append(frame)
            cv2.imwrite('snake_' + str(count) + str('.png'), frame)
        else:
            break
        count += 1
        shift += 5

    cap.release()

def edit_video():
    print('edit...')

if __name__ == '__main__':
    thread_read = threading.Thread(target = read_video, args = ([file_name]))
    thread_edit = threading.Thread(target = edit_video)

    thread_read.start()
    thread_edit.start()

