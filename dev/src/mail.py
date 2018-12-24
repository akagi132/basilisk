import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import datetime

FROM_ADDRESS = 'basilisk.system@gmail.com'
MY_PASSWORD = 'basilisk_system10'
TO_ADDRESS = 'akagi13213a@gmail.com'
BODY = 'harp move.'

def create_message(from_addr, to_addr, body):
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    msg = MIMEText(body)
    msg['Subject'] = 'basilisk_system ' + now
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()
    return msg

def send(from_addr, to_addrs, msg):
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(FROM_ADDRESS, MY_PASSWORD)
    smtpobj.sendmail(from_addr, to_addrs, msg.as_string())
    smtpobj.close()

if __name__ == '__main__':

    to_addr = TO_ADDRESS
    body = BODY

    msg = create_message(FROM_ADDRESS, to_addr, body)
    send(FROM_ADDRESS, to_addr, msg)

