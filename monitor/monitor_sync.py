#!/bin/env python
#coding:gbk

from item import *
from common_fun import *
from sendmail import *

#判断同步连接数是否正常
def isSync(localIp, localPort, remoteIp, remotePort):
    basecmd = 'netstat -an | grep ESTABLISHED | egrep'

    filter_ip = '%s:%s.*%s:|%s:.*%s:%s' % (
            localIp, localPort, remoteIp,
            localIp, remoteIp, remotePort)

    judgeCmd = "%s '%s'" % (basecmd, filter_ip)
    log.info('执行%s服务器命令:[%s]，判断连接数', localIp, judgeCmd)
    (returncode, out_lines) = sshIpCmd(localIp, judgeCmd)

    connectCount = len(out_lines)
    if connectCount < 2:
       msg = '根据服务器:%s的连接数分析，数据同步出问题，需要服务器:%s重启同步\n' % (
                localIp, remoteIp)
       msg += '命令：%s 输出如下：\n' % judgeCmd
       msg += '\n'.join(out_lines)
       log.error(msg)
       return False
    else:
       log.info('执行%s服务器命令:[%s]，连接数正常，数量为:[%d]', localIp, judgeCmd, connectCount)
       return True

#重启数据库连接
def restartSync(ip, port, dbname):
    cmd = "/home/maintainer/monitor/basecmd.sh resync %d" % (port)
    (returncode, out_lines) = sshIpCmd(ip, cmd)

    log.error('已重启%s服务器%d端口%s库的同步服务' % (ip, port, dbname))


def main():
    for dbname, dbhost_map in db_map.items():
        masterNode = dbhost_map.get('master')
        slaveNode = dbhost_map.get('slave')
        masterName = masterNode[0]
        masterPort = masterNode[1]
        slaveName = slaveNode[0]
        slavePort = slaveNode[1]
        masterHostItems = host_map.get(masterName)
        masterHostIp = masterHostItems[1]
        slaveHostItems = host_map.get(slaveName)
        slaveHostIp = slaveHostItems[1]

        msg = '%s %s 监测%s: master:%s:%s:%d \n slave:%s:%s:%d\n' % (today(), now(), dbname,
            masterName, masterHostIp, masterPort, slaveName, slaveHostIp, slavePort)

        #判断主服务同步连接数
        if not isSync(masterHostIp, masterPort, slaveHostIp, slavePort):
            restartSync(slaveHostIp, slavePort, dbname)
            if not isSync(masterHostIp, masterPort, slaveHostIp, slavePort):
                sendmail('告警：数据库同步异常', msg)
                log.error('告警：数据库同步异常:[%s]' % msg)

        #判断从服务同步连接数
        if not isSync(slaveHostIp, slavePort, masterHostIp, masterPort):
            restartSync(masterHostIp, masterPort, dbname)
            if not isSync(slaveHostIp, slavePort, masterHostIp, masterPort):
                sendmail('告警：数据库同步异常', msg)
                log.error('告警：数据库同步异常:[%s]' % msg)


def main2():

    basecmd = 'netstat -an | grep ESTABLISHED | egrep'

    for dbname, dbhost_map in db_map.items():
        masterNode = dbhost_map.get('master')
        slaveNode = dbhost_map.get('slave')
        masterName = masterNode[0]
        masterPort = masterNode[1]
        slaveName = slaveNode[0]
        slavePort = slaveNode[1]
        masterHostItems = host_map.get(masterName)
        masterHostIp = masterHostItems[1]
        slaveHostItems = host_map.get(slaveName)
        slaveHostIp = slaveHostItems[1]

        msg = '%s %s 监测%s: master:%s:%s:%d \n slave:%s:%s:%d\n' % (today(), now(), dbname,
            masterName, masterHostIp, masterPort, slaveName, slaveHostIp, slavePort)

        filter_ip = '%s:%s.*%s:|%s:.*%s:%s' % (
            masterHostIp, masterPort, slaveHostIp,
            masterHostIp, slaveHostIp, slavePort)

        sshcmd = "%s '%s'" % (basecmd, filter_ip)
        (returncode, master_out_lines) = sshIpCmd(masterHostIp, sshcmd)
        masterConnectCount = len(master_out_lines)

        status = True
        if masterConnectCount < 2:
            msg += '根据服务器:%s的连接数分析，数据同步出问题，需要服务器:%s重启同步\n' % (
                masterHostIp, slaveHostIp)
            msg += '命令：%s 输入如下：\n' % sshcmd
            msg += '\n'.join(master_out_lines)

            cmd = 'ssh root@%s "/home/maintainer/monitor/basecmd.sh resync %d"' % (slaveHostIp, slavePort)
            (returncode, out_lines) = execute_command(cmd)
            log.info('已重启%s服务器%d端口%s库的同步服务' % (slaveHostIp, slavePort, dbname))
            status = False

        filter_ip = '%s:%s.*%s:|%s:.*%s:%s' % (
            slaveHostIp, slavePort, masterHostIp,
            slaveHostIp, masterHostIp, masterPort)

        sshcmd = "%s '%s'" % (basecmd, filter_ip)
        (returncode, slave_out_lines) = sshIpCmd(slaveHostIp, sshcmd)
        slaveConnectCount = len(slave_out_lines)

        if slaveConnectCount < 2:
            msg += '根据服务器:%s的连接数分析，数据同步出问题，需要服务器:%s重启同步\n' % (
                slaveHostIp, masterHostIp)
            msg += '命令：%s 输入如下：\n' % sshcmd
            msg += '\n'.join(slave_out_lines)

            cmd = 'ssh root@%s "/home/maintainer/monitor/basecmd.sh resync %d"' % (masterHostIp, masterPort)
            (returncode, out_lines) = execute_command(cmd)
            log.info('已重启%s服务器%d端口%s库的同步服务' % (masterHostIp, masterPort, dbname))

            status = False
        if not status:
            if dbname != "dd8989":
                sendmail('告警：数据库同步异常', msg)
            log.error('告警：数据库同步异常 [%s]' % msg)

if __name__ == '__main__':
    main()
