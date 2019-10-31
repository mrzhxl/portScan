#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import sys
import os
import requests
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import conf

WeixinAlertUrl = conf.CONFIG.get('weixin').get('WeixinAlertUrl')

def sendMail(address, sub, content):
    mail_from = conf.CONFIG.get('email').get('email_username')
    smtpserver = conf.CONFIG.get('email').get('email_host')
    user = conf.CONFIG.get('email').get('email_username')
    pwd = conf.CONFIG.get('email').get('email_password')
    message = MIMEText(content, 'html', 'utf-8')
    message['From'] = Header(mail_from, 'utf-8')
    message['To'] = Header(address, 'utf-8')
    message['Subject'] = Header(sub, 'utf-8')

    sm = smtplib.SMTP_SSL(smtpserver, 465)
    sm.login(user,pwd)
    sm.sendmail(mail_from, address, message.as_string())
    sm.quit()


def weixin_alert(users,message):
    for user in users:
        data = {'method': 'wechat', 'user': user, 'message': message}
        req = requests.post(WeixinAlertUrl,data=data)


def main():
    if len(sys.argv) != 4:
        print("Usage %s address sub content" % sys.argv[0])
        sys.exit(10)

    address = sys.argv[1]
    sub = sys.argv[2]
    content = sys.argv[3]
    sendMail(address, sub, content)

if __name__ == '__main__':
    main()
