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
        #在0点到8点，邮件进缓存
        msg = '延迟发送%s %s的邮件：%s\n %s' % (today(), now(), subject, content)
        cache.lpush(key, msg)
        return

    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  #设置服务器
    mail_user = "monitor_smtp@qq.com"    #用户名
    mail_pass = "8ik,9ol.0p;/"   #口令
    mail_user = "69617457@qq.com"    #用户名
    mail_pass = "dir9dir12"   #口令

    sender = '69617457@qq.com'
    receivers = ['69617457@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    while cache.llen(key) > 0:
        content += '\n\n===============================================\n'
        content += cache.lpop(key)

    message = MIMEText(content, 'plain', 'gbk')
    message['From'] = Header("监控告警", 'gbk')
    message['To'] = Header("处理人员", 'gbk')

    # subject = 'Python SMTP 邮件测试'
    message['Subject'] = Header(subject, 'gbk')

    try:
        smtpObj = SMTP_SSL(mail_host, 465)
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        # print "邮件发送成功"
        # print content
    except smtplib.SMTPException, e:
        print "Error: 无法发送邮件"


def main():
    sendmail('服务器异常重启', '告警：服务器g2m:112.213.126.135已重启，本次重启时间：2016-08-02 09时，上次启动时间：20160802 09')

if __name__ == '__main__':
    main()