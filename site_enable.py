#!/usr/local/bin/python
#coding=gbk

import sys, os, time, datetime
import re
import httplib
import commands

httpClient = None
site_list = [
    '103.20.195.125',
    'byy99.ddk11.com',
    'xyy989.wkg99.com',
    'wyy909.yhh389.com',
    # 'w2.bvbv66.com',
    'bdd99.waa789.com',
    '112.213.126.135',
    '59.188.133.54',
    '103.247.165.144'
]


def execute_command(cmdstring):
    # 一种Shell命令执行方法
    returncode, out = commands.getstatusoutput(cmdstring)
    out_lines = out.split('\n')

    return returncode, out_lines


def dns2ip(dns):
    ip = ''
    cmd = 'ping -c 1 %s' % dns
    returncode, lines = execute_command(cmd)
    if returncode != 0:
        print '%s 域名解释出错' % cmd
    else:
        patt = re.compile(r'.*\((\d+\.\d+\.\d+\.\d+)\)')
        m = patt.match(lines[0])
        if m:
            ip = m.group(1)
            print '%s   =====>   %s' % (dns, ip)
    return ip


def check(site):
    try:
        print "===============%s================" % site
        httpClient = httplib.HTTPConnection(site, 80, timeout=30)
        httpClient.request('GET', '/')

        #response是HTTPResponse对象
        response = httpClient.getresponse()
        print response.status
        print response.reason
        # print response.read()
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()

def main():
    for site in site_list:
        print "\n\n"
        dns2ip(site)
        check(site)

if __name__ == '__main__':
    main()
