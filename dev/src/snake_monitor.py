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

FROM_ADDRESS = 'basilisk.system@gmail.com'
MY_PASSWORD = 'basilisk_system10'
TO_ADDRESS = 'akagi13213a@gmail.com'
BODY = 'harp move.'

raw_image = None

def create_message(body):
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    msg = MIMEMultipart()
    msg['Subject'] = 'basilisk_system ' + now
    msg['From'] = FROM_ADDRESS
    msg['To'] = TO_ADDRESS
    msg['Date'] = formatdate()
    msg.attach(MIMEText(body))

    attachment = MIMEBase('image', 'png')
    file = open('/home/fokko/snake_system/dev/src/dist.png', 'rb+')
    attachment.set_payload(file.read())
    file.close()
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', filename='dist.png')
    msg.attach(attachment)

    return msg

def send(msg):
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(FROM_ADDRESS, MY_PASSWORD)
    smtpobj.sendmail(FROM_ADDRESS, TO_ADDRESS, msg.as_string())
    smtpobj.close()

def getImage(cap):
    (ret, frame) = cap.read()
    if ret:
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        print('usb cam read error...')
        img = []
    global raw_image
    raw_image = frame
    return img

def getSimilarity(target_img, compare_img, threshold, save_image=True):
    width = int(target_img.shape[1])
    height = int(target_img.shape[0])

    dist_img = raw_image.copy()
    sim = 0
    sim_n = 0

    for i in range(height):
        for j in range(width):
            sub = abs(int(target_img[i, j]) - int(compare_img[i, j]))
            if (sub > threshold):
                sim_n += 1
                sim += sub
                dist_img[i, j] = [0, 255, 0]

    return (sim_n, sim)

def main(cam, interval, threshold):
    cap = cv2.VideoCapture(cam)
    last_image = getImage(cap)

    while True:
        frame = getImage(cap)
        (sim_n, similarity) = getSimilarity(frame, last_image, threshold, save_image=True)
        
        print(sim_n)
        print(similarity)
        last_image = frame

        if sim_n > 0:
            body = BODY + '\n' + 'similarity:' + str(similarity) + '\n' + 'sim_n:' + str(sim_n) + '\n' + 'interval[s]:' + str(interval) + '\n' + 'threshold:' + str(threshold)
            msg = create_message(body)

            thread = threading.Thread(target=send, args=([msg]))
            thread.start()

        sleep(interval)

    cap.release()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('please set src image and compare image')
    else:
        args = sys.argv
        TARGET_CAM = int(args[1])
        INTERVAL_MIN = int(args[2])
        THRESHOLD = int(args[3])

        if INTERVAL_MIN < 1:
            print('please set interval larger than 1')
        else:
            main(TARGET_CAM, INTERVAL_MIN, THRESHOLD)

