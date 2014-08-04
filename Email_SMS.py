#Author: Colin Gerber
#env: python 2.7

__version__ = 1.0

import smtplib, os
from email.MIMEMultipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import time
import config

def send_mail(send_from, send_to, subject, text,smtp, files=[]):
    assert isinstance(send_to, list)
    assert isinstance(files, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach( MIMEText(text) )

    for f in files:
        part = MIMEApplication(open(f, 'rb').read())
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)

    server = smtplib.SMTP(smtp)
    server.ehlo()
    server.starttls()
    server.login(config.email['username'], config.email['password'])
    server.sendmail(send_from, send_to, msg.as_string())
    server.close()

def send_text(phone_number, msg):
    fromaddr = "Address"
    toaddrs = phone_number + "@txt.att.net"
    msg = ("From: {0}\r\nTo: {1}\r\n\r\n{2}").format(fromaddr, toaddrs, msg)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(config.email['username'], config.email['password'])
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

def main(fname):
    date = time.strftime("%m/%d/%Y")
    send_from = 'sender'
    send_to = ['recipients']
    subject = 'subject'
    text = 'Message text'
    files=[fname]
    smtp='smtp.gmail.com:587'
    send_mail(send_from, send_to, subject, text,smtp, files)

    print 'Email Sent'

if __name__ == "__main__":
    main()
