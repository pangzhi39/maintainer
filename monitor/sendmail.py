#!/bin/env python
#coding:gbk

import smtplib
import redis
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
from common_fun import *


def sendmail(subject, content):
    cache = redis.StrictRedis('127.0.0.1', 6379)
    key = 'mail|waitsend'

    if now() > '00:00:00' and now () < '08:00:00':
        #��0�㵽8�㣬�ʼ�������
        msg = '�ӳٷ���%s %s���ʼ���%s\n %s' % (today(), now(), subject, content)
        cache.lpush(key, msg)
        return

    # ������ SMTP ����
    mail_host = "smtp.qq.com"  #���÷�����
    mail_user = "monitor_smtp@qq.com"    #�û���
    mail_pass = "8ik,9ol.0p;/"   #����
    mail_user = "69617457@qq.com"    #�û���
    mail_pass = "dir9dir12"   #����

    sender = '69617457@qq.com'
    receivers = ['69617457@qq.com']  # �����ʼ���������Ϊ���QQ���������������

    while cache.llen(key) > 0:
        content += '\n\n===============================================\n'
        content += cache.lpop(key)

    message = MIMEText(content, 'plain', 'gbk')
    message['From'] = Header("��ظ澯", 'gbk')
    message['To'] = Header("������Ա", 'gbk')

    # subject = 'Python SMTP �ʼ�����'
    message['Subject'] = Header(subject, 'gbk')

    try:
        smtpObj = SMTP_SSL(mail_host, 465)
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        # print "�ʼ����ͳɹ�"
        # print content
    except smtplib.SMTPException, e:
        print "Error: �޷������ʼ�"


def main():
    sendmail('�������쳣����', '�澯��������g2m:112.213.126.135����������������ʱ�䣺2016-08-02 09ʱ���ϴ�����ʱ�䣺20160802 09')

if __name__ == '__main__':
    main()