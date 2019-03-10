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

FROM_ADDRESS = 'basilisk.system@gmail.com'      # 送信元メールアドレス
MY_PASSWORD = 'basilisk_system10'                         # 送信元メールアドレスのパスワード
TO_ADDRESS = 'akagi13213a@gmail.com'                 # 送信先メールアドレス

def create_message(body):
    # 本文の作成
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S') # 時刻
    msg = MIMEMultipart()                                   # 添付ファイル付きメールとしてメッセージ作成
    msg['Subject'] = 'basilisk_system ' + now   # 題名
    msg['From'] = FROM_ADDRESS                  # 差出人
    msg['To'] = TO_ADDRESS                      # 宛先
    msg['Date'] = formatdate()                  # 時刻
    msg.attach(MIMEText(body))                  # 本文

    attachment = MIMEBase('image', 'png')       # 画像(png)を添付することを明示
    file = open('/home/fokko/basilisk/dev/src/dist.png', 'rb+') #rb+:バイナリ読み込み
    attachment.set_payload(file.read())         # 画像を添付
    file.close()
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', filename='dist.png')
    msg.attach(attachment)

    return msg

def send(msg):
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)   # gmail から送信
    smtpobj.ehlo()          # おまじない
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(FROM_ADDRESS, MY_PASSWORD)    # 差出人アドレスにログイン
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
    return (frame, img) # カラー画像とグレー画像

def getSimilarity(raw_img, target_img, compare_img, threshold):
    width = int(target_img.shape[1])
    height = int(target_img.shape[0])

    dist_img = raw_img.copy()
    sim = 0     # 輝度差の合計
    sim_n = 0   # 輝度差が threshold を超えた画素数

    for i in range(height):
        for j in range(width):
            sub = abs(int(target_img[i, j]) - int(compare_img[i, j]))
            if (sub > threshold):
                sim_n += 1
                sim += sub
                dist_img[i, j] = [0, 255, 0]    # 輝度差がしきい値を超えた画素は、緑で塗る
    cv2.imwrite('dist.png', dist_img);
    return (sim_n, sim)

def main(cam, interval, threshold):
    cap = cv2.VideoCapture(cam)     # USBカメラから映像読み込み
    (raw_img, last_img) = getImage(cap)

    while True:
        (raw_img, frame) = getImage(cap)       # USBカメラの画像取得
        (sim_n, similarity) = getSimilarity(raw_img, frame, last_img, threshold)    # 類似度算出
        
        print('sim_n', sim_n);
        
        last_img = frame

        if sim_n > 0:
            # メール処理
            body = 'similarity:' + str(similarity) + '\n' + 'sim_n:' + str(sim_n) + '\n' + 'interval[s]:' + str(interval) + '\n' + 'threshold:' + str(threshold)
            msg = create_message(body)

            # メール送信を別スレッドで行う
            thread = threading.Thread(target=send, args=([msg]))
            thread.start()

        sleep(interval)

    cap.release()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('please set camera num, interval min, threshold.')
    else:
        args = sys.argv
        TARGET_CAM = int(args[1])   # USBカメラ番号（内臓カメラは0, USBカメラは1, 2, 3.. と続く）
        INTERVAL_SEC = int(args[2]) # 更新間隔
        THRESHOLD = int(args[3])    # 比較のしきい値

        if INTERVAL_SEC < 1:
            print('please set interval larger than 1')
        else:
            main(TARGET_CAM, INTERVAL_SEC, THRESHOLD)
