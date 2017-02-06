#!/bin/env python
#coding:gbk

import redis
from item import *
from common_fun import *
from sendmail import *

def main():
    cache = redis.StrictRedis('127.0.0.1', 6379)

    cmdpath = '/home/maintainer/monitor'
    cmd = '"%s/basecmd.sh up_h"' % (cmdpath)

    host_list = host_map.keys()
    host_list.sort()
    for name in host_list:
        host_set = host_map.get(name)
        key = 'restart|%s' % (name)
        if cache.exists(key):
            up_time = cache.get(key)
        else:
            up_time = '0'

        ip1 = host_set[1]
        
        (returncode, out_lines) = sshIpCmd(ip1, cmd)
        if returncode == 0:
            value_list = out_lines[0].split('|')

            curr_up_time = value_list[0]
            display_up_time = value_list[1]
            #�ж�����ʱ���Ƿ����60��
            if abs(int(up_time) - int(curr_up_time)) > 30:
                #��ʾ�����ʼ�֪ͨ
                msg = '������%s:%s������������ʱ�䣺%s��ԭ����ʱ�䣺%s, Ӱ�����ݿ⣺%s' % (
                    name, ip1, display_up_time, up_time, 
                    '��'.join(getDbFormHost(name)))
                sendmail('�澯���������쳣����', msg)
                # print msg
                cache.set(key, curr_up_time)
        else:
            print "����ִ�г��� %d " % (returncode)
            print out_lines


if __name__ == '__main__':
    main()
