#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import datetime
from time import sleep
import sys
import smtplib
import numpy as np
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
import threading

FROM_ADDRESS = 'basilisk.system@gmail.com'      # ���M�����[���A�h���X
MY_PASSWORD = 'basilisk_system10'                         # ���M�����[���A�h���X�̃p�X���[�h
TO_ADDRESS = 'akagi13213a@gmail.com'                 # ���M�惁�[���A�h���X

def create_message(body):
    # �{���̍쐬
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S') # ����
    msg = MIMEMultipart()                                   # �Y�t�t�@�C���t�����[���Ƃ��ă��b�Z�[�W�쐬
    msg['Subject'] = 'basilisk_system ' + now   # �薼
    msg['From'] = FROM_ADDRESS                  # ���o�l
    msg['To'] = TO_ADDRESS                      # ����
    msg['Date'] = formatdate()                  # ����
    msg.attach(MIMEText(body))                  # �{��

    attachment = MIMEBase('image', 'png')       # �摜(png)��Y�t���邱�Ƃ𖾎�
    file = open('/home/fokko/basilisk/dev/src/dist.png', 'rb+') #rb+:�o�C�i���ǂݍ���
    attachment.set_payload(file.read())         # �摜��Y�t
    file.close()
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', filename='dist.png')
    msg.attach(attachment)

    return msg

def send(msg):
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)   # gmail ���瑗�M
    smtpobj.ehlo()          # ���܂��Ȃ�
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(FROM_ADDRESS, MY_PASSWORD)    # ���o�l�A�h���X�Ƀ��O�C��
    smtpobj.sendmail(FROM_ADDRESS, TO_ADDRESS, msg.as_string())
    print('send.');
    smtpobj.close()

def getImage(cap):
    (ret, frame) = cap.read()
    if ret:
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        print('usb cam read error...')
        img = []
    return (frame, img) # �J���[�摜�ƃO���[�摜

def getSimilarity(raw_img, target_img, compare_img, threshold):
    width = int(target_img.shape[1])
    height = int(target_img.shape[0])

    dist_img = raw_img.copy()
    sim = 0     # �P�x���̍��v
    sim_n = 0   # �P�x���� threshold �𒴂�����f��

    for i in range(height):
        for j in range(width):
            sub = abs(int(target_img[i, j]) - int(compare_img[i, j]))
            if (sub > threshold):
                sim_n += 1
                sim += sub
                dist_img[i, j] = [0, 255, 0]    # �P�x�����������l�𒴂�����f�́A�΂œh��
    cv2.imwrite('dist.png', dist_img);
    return (sim_n, sim)

def main(cam, interval, threshold):
    cap = cv2.VideoCapture(cam)     # USB�J��������f���ǂݍ���
    (raw_img, last_img) = getImage(cap)

    while True:
        (raw_img, frame) = getImage(cap)       # USB�J�����̉摜�擾
        (sim_n, similarity) = getSimilarity(raw_img, frame, last_img, threshold)    # �ގ��x�Z�o
        
        print('sim_n', sim_n);
        
        last_img = frame

        if sim_n > 0:
            # ���[������
            body = 'similarity:' + str(similarity) + '\n' + 'sim_n:' + str(sim_n) + '\n' + 'interval[s]:' + str(interval) + '\n' + 'threshold:' + str(threshold)
            msg = create_message(body)

            # ���[�����M��ʃX���b�h�ōs��
            thread = threading.Thread(target=send, args=([msg]))
            thread.start()

        sleep(interval)

    cap.release()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('please set camera num, interval min, threshold.')
    else:
        args = sys.argv
        TARGET_CAM = int(args[1])   # USB�J�����ԍ��i�����J������0, USB�J������1, 2, 3.. �Ƒ����j
        INTERVAL_SEC = int(args[2]) # �X�V�Ԋu
        THRESHOLD = int(args[3])    # ��r�̂������l

        if INTERVAL_SEC < 1:
            print('please set interval larger than 1')
        else:
            main(TARGET_CAM, INTERVAL_SEC, THRESHOLD)
