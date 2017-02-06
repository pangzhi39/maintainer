#!/bin/env python
#coding:gbk

from item import *
from common_fun import *
from sendmail import *

#�ж�ͬ���������Ƿ�����
def isSync(localIp, localPort, remoteIp, remotePort):
    basecmd = 'netstat -an | grep ESTABLISHED | egrep'

    filter_ip = '%s:%s.*%s:|%s:.*%s:%s' % (
            localIp, localPort, remoteIp,
            localIp, remoteIp, remotePort)

    judgeCmd = "%s '%s'" % (basecmd, filter_ip)
    log.info('ִ��%s����������:[%s]���ж�������', localIp, judgeCmd)
    (returncode, out_lines) = sshIpCmd(localIp, judgeCmd)

    connectCount = len(out_lines)
    if connectCount < 2:
       msg = '���ݷ�����:%s������������������ͬ�������⣬��Ҫ������:%s����ͬ��\n' % (
                localIp, remoteIp)
       msg += '���%s ������£�\n' % judgeCmd
       msg += '\n'.join(out_lines)
       log.error(msg)
       return False
    else:
       log.info('ִ��%s����������:[%s]������������������Ϊ:[%d]', localIp, judgeCmd, connectCount)
       return True

#�������ݿ�����
def restartSync(ip, port, dbname):
    cmd = "/home/maintainer/monitor/basecmd.sh resync %d" % (port)
    (returncode, out_lines) = sshIpCmd(ip, cmd)

    log.error('������%s������%d�˿�%s���ͬ������' % (ip, port, dbname))


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

        msg = '%s %s ���%s: master:%s:%s:%d \n slave:%s:%s:%d\n' % (today(), now(), dbname,
            masterName, masterHostIp, masterPort, slaveName, slaveHostIp, slavePort)

        #�ж�������ͬ��������
        if not isSync(masterHostIp, masterPort, slaveHostIp, slavePort):
            restartSync(slaveHostIp, slavePort, dbname)
            if not isSync(masterHostIp, masterPort, slaveHostIp, slavePort):
                sendmail('�澯�����ݿ�ͬ���쳣', msg)
                log.error('�澯�����ݿ�ͬ���쳣:[%s]' % msg)

        #�жϴӷ���ͬ��������
        if not isSync(slaveHostIp, slavePort, masterHostIp, masterPort):
            restartSync(masterHostIp, masterPort, dbname)
            if not isSync(slaveHostIp, slavePort, masterHostIp, masterPort):
                sendmail('�澯�����ݿ�ͬ���쳣', msg)
                log.error('�澯�����ݿ�ͬ���쳣:[%s]' % msg)


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

        msg = '%s %s ���%s: master:%s:%s:%d \n slave:%s:%s:%d\n' % (today(), now(), dbname,
            masterName, masterHostIp, masterPort, slaveName, slaveHostIp, slavePort)

        filter_ip = '%s:%s.*%s:|%s:.*%s:%s' % (
            masterHostIp, masterPort, slaveHostIp,
            masterHostIp, slaveHostIp, slavePort)

        sshcmd = "%s '%s'" % (basecmd, filter_ip)
        (returncode, master_out_lines) = sshIpCmd(masterHostIp, sshcmd)
        masterConnectCount = len(master_out_lines)

        status = True
        if masterConnectCount < 2:
            msg += '���ݷ�����:%s������������������ͬ�������⣬��Ҫ������:%s����ͬ��\n' % (
                masterHostIp, slaveHostIp)
            msg += '���%s �������£�\n' % sshcmd
            msg += '\n'.join(master_out_lines)

            cmd = 'ssh root@%s "/home/maintainer/monitor/basecmd.sh resync %d"' % (slaveHostIp, slavePort)
            (returncode, out_lines) = execute_command(cmd)
            log.info('������%s������%d�˿�%s���ͬ������' % (slaveHostIp, slavePort, dbname))
            status = False

        filter_ip = '%s:%s.*%s:|%s:.*%s:%s' % (
            slaveHostIp, slavePort, masterHostIp,
            slaveHostIp, masterHostIp, masterPort)

        sshcmd = "%s '%s'" % (basecmd, filter_ip)
        (returncode, slave_out_lines) = sshIpCmd(slaveHostIp, sshcmd)
        slaveConnectCount = len(slave_out_lines)

        if slaveConnectCount < 2:
            msg += '���ݷ�����:%s������������������ͬ�������⣬��Ҫ������:%s����ͬ��\n' % (
                slaveHostIp, masterHostIp)
            msg += '���%s �������£�\n' % sshcmd
            msg += '\n'.join(slave_out_lines)

            cmd = 'ssh root@%s "/home/maintainer/monitor/basecmd.sh resync %d"' % (masterHostIp, masterPort)
            (returncode, out_lines) = execute_command(cmd)
            log.info('������%s������%d�˿�%s���ͬ������' % (masterHostIp, masterPort, dbname))

            status = False
        if not status:
            if dbname != "dd8989":
                sendmail('�澯�����ݿ�ͬ���쳣', msg)
            log.error('�澯�����ݿ�ͬ���쳣 [%s]' % msg)

if __name__ == '__main__':
    main()
