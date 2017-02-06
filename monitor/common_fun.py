#!/usr/bin/env python
#coding:gbk
'''
    常用函数库           2016.2.27
'''

import sys, os, time, datetime
import platform
import socket
import subprocess
import shlex
import logging
import logging.config
import commands


# 日志类定义
logging.config.fileConfig("/home/maintainer/monitor/log.conf")
log = logging.getLogger()
# 取主机名
hostname = socket.gethostname()
save_path = './'


def today(fmt='%Y%m%d'):
    '''取当前日期字符串YYYYMMDD'''
    t = time.strftime(fmt, time.localtime())
    return t


def now():
    return today('%H:%M:%S')


def dateCalc(strDate, iDay, fmt='%Y%m%d'):
    ''' 日期运算 '''
    chkDate = time.strptime(strDate, fmt)
    dateTmp = datetime.datetime(chkDate[0], chkDate[1], chkDate[2])
    resultDate = dateTmp + datetime.timedelta(days=iDay)
    return datetime.date.strftime(resultDate, fmt)


def execute_command(cmdstring, cwd=None, timeout=None, shell=True):
    """执行一个SHELL命令
            封装了subprocess的Popen方法, 支持超时判断，支持读取stdout和stderr
           参数:
        cwd: 运行命令时更改路径，如果被设定，子进程会直接先更改当前路径到cwd
        timeout: 超时时间，秒，支持小数，精度0.1秒
        shell: 是否通过shell运行
    Returns: return_code
    Raises:  Exception: 执行超时
    """
    if shell:
        cmdstring_list = cmdstring
    else:
        cmdstring_list = shlex.split(cmdstring)
    if timeout:
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

    log.info('开始在主机:[%s]上执行Shell命令:[%s]' % (hostname, cmdstring))

    # 另外一种Shell命令执行方法
    returncode, out = commands.getstatusoutput(cmdstring)
    # returncode, out = commands.getstatusoutput('dir')
    # print out
    out_lines = out.split('\n')
    err_lines = []
    # print returncode
    # print out_lines

    #没有指定标准输出和错误输出的管道，因此会打印到屏幕上；
    # sub = subprocess.Popen(cmdstring_list, cwd=cwd, 
    #     stdin=subprocess.PIPE,
    #     stdout=subprocess.PIPE,
    #     stderr=subprocess.PIPE,
    #     shell=shell,bufsize=1024000)
    
    # #subprocess.poll()方法：检查子进程是否结束了，如果结束了，设定并返回码，放在subprocess.returncode变量中 
    # while sub.poll() is None:
    #     time.sleep(0.1)
    #     if timeout:
    #         if end_time <= datetime.datetime.now():
    #             raise Exception("Timeout：%s"%cmdstring)
     
    # out_lines = sub.stdout.readlines()
    # err_lines = sub.stderr.readlines()
    # returncode = sub.returncode

    log.info('完成在主机:[%s]上执行Shell命令:[%s], 返回值:[%d]' % (hostname, cmdstring, returncode))


    # cmd = cmdstring.split(' ')[0]
    # result_file_name = '%s/%s%s' % (save_path, cmd, today('_%H%M%S'))
    # f = open(result_file_name, 'w')

    # f.write('---------------shell---------------------\n')
    # f.write(cmdstring + '\n')
    # f.write('---------------------------------------\n')
    # f.write('return code:[%d]\n' % returncode)
    # f.write('--------------stdout--------------------\n')
    # for line in out_lines:
    #     f.write(line + '\n')
    # f.write('--------------stderr-------------------\n')
    # for line in err_lines:
    #     f.write(line + '\n')
    # f.close()

    return (returncode, out_lines)


class CommonError(Exception):
    """公共异常类"""
    def __init__(self, code="", msg=""):
        self.code = code
        self.msg = msg
        
    def __repr__(self):
        return '自定义出错信息%s:%s' % self.code, self.msg


def isLinux():
    # print platform.system()
    if platform.system() == 'Linux':
        return True
    else:
        return False


def main():
    # returncode, out_lines = execute_command('ls ./')
    # for line in out_lines:
    #     print line
    #returncode, out_lines = execute_command('ping -n 1 192.168.19.130')
    print today('%H%M%S')
    pass


if __name__ == '__main__':
    main()
