#!/bin/env python
#coding:gbk

import time
import logging
import logging.config
import commands

# 日志类定义
logging.config.fileConfig("/home/maintainer/monitor/log.conf")
log = logging.getLogger()

host_map = {
    'g1m' : ('S210245214246', '59.188.43.8'),
    'g1s' : ('S103250152829', '103.250.15.58', '103.250.15.59'),
    'g2m' : ('localhost', '112.213.126.135', '112.213.126.136', '112.213.126.137'),
    'g2s' : ('S43243512425', '43.243.51.40', '43.243.51.41'),
    'g4m' : ('localhost', '103.20.195.125'),
    'g5m' : ('P210245214242243', '210.245.214.162'),
    'g6m' : ('s210245214165', '210.245.214.199', '210.245.214.198'),
    'g6s' : ('S10325015196', '103.250.15.66', '103.250.15.66'),
}

db_map = {
    'dd3840': {'master':('g1m', 3306), 'slave':('g1s', 3306)},
    'dd5670': {'master':('g2m', 3306), 'slave':('g2s', 3307)},
    'dd8989': {'master':('g4m', 3306), 'slave':('g1s', 3307)},
    'dd3855': {'master':('g5m', 3306), 'slave':('g2s', 3306)},
    'dd5120': {'master':('g6m', 3306), 'slave':('g6s', 3306)},
}

def getDbFormHost(name):
    db_list = []
    for dbname, dbhost_map in db_map.items():
        masterNode = dbhost_map.get('master')
        slaveNode = dbhost_map.get('slave')
        masterName = masterNode[0]
        slaveName = slaveNode[0]
        if name == masterName:
            db_list.append(dbname)
        if name == slaveName:
            db_list.append(dbname)

    return db_list

def sshHostCmd(host, cmd):
    hostItem = host_map.get(host)
    ip = hostItem[1]

    return sshIpCmd(ip, cmd)


def sshIpCmd(ip, cmd):
    sshCmd = '''ssh root@%s "%s" ''' % (ip, cmd)
    delayList = [0, 3, 10, 60]
    out_lines = []

    for delay in delayList:
        time.sleep(delay)
        returncode, out = commands.getstatusoutput(sshCmd)
        # 执行超时，则先延时再次重试
        if out.find('Connection timed out') == -1:
           continue

        out_lines = out.split('\n')
        log.info('执行Shell命令:[%s], 返回值:[%d], 返回信息:[%s]' % (
            sshCmd, returncode, out))
        break

    return (returncode, out_lines)

def main():
    for name, host_set in host_map.items():
        print name, host_set
    for dbname, sotre_server_map in db_map.items():
        print dbname, sotre_server_map        
    pass

    print getDbFormHost('g2s')

if __name__ == '__main__':
    main()
