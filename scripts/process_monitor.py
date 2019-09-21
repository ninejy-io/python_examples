#!/usr/bin/env python3
# coding: utf-8
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header

local_ip = "172.31.39.251"
sender = "send@163.com"
receivers = ["recv@qq.com"]


def send_mail(info, num=0):
    msg = MIMEText("Host: {}\n\nProcessName: {}\n\nStatus: down\n\nValue: {}".format(local_ip, info, num), 'plain', 'utf-8')
    msg['Subject'] = Header("{} process down".format(info), 'utf-8')
    msg['From'] = Header("{} Process Down".format(info), "utf-8")
    msg['To'] = Header("sysadmin", "utf-8")

    server = smtplib.SMTP()
    server.connect('smtp.163.com', '25')
    server.starttls()
    server.login(sender, 'password-xxx')
    server.sendmail(sender, receivers, msg.as_string())
    server.quit()

def check_process(process_name):
    ret = os.popen('ps -ef |grep -v grep|grep {}|wc -l'.format(process_name))
    num = ret.read().strip('\n')
    print(num)
    if int(num) == 1:
       send_mail(process_name, num)


if __name__ == '__main__':
    while True:
        time.sleep(60)
        check_process('ssserver')
