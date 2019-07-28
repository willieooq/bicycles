# !/usr/bin/python 
# -*-coding:utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(totx,subjecttx,bodytx):

    msg = MIMEMultipart()
    msg['From'] = "brokenbikeline@gmail.com"
    msg['To'] = totx
    msg['Subject'] = subjecttx
    msg.attach(MIMEText(bodytx, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("brokenbikeline@gmail.com", "brokenbike")
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print("a email sent.")
    except:
        print("something wrong!\n")
        print("sent:"+ msg.as_string())

