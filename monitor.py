#!/usr/local/bin/python
#coding:gbk

import sys, os, time, datetime
import re
import platform
import commands
import logging
import logging.config
import MySQLdb


# 日志类定义
logging.config.fileConfig("/home/maintainer/log.conf")
log = logging.getLogger()


def today(fmt='%Y%m%d'):
    '''取当前日期字符串YYYYMMDD'''
    t = time.strftime(fmt, time.localtime())
    return t

def dateCalc(strDate, iDay, fmt='%Y%m%d'):
    ''' 日期运算 '''
    chkDate = time.strptime(strDate, fmt)
    dateTmp = datetime.datetime(chkDate[0], chkDate[1], chkDate[2])
    resultDate = dateTmp + datetime.timedelta(days=iDay)
    return datetime.date.strftime(resultDate, fmt)

def execute_command(cmdstring):
    # 一种Shell命令执行方法
    returncode, out = commands.getstatusoutput(cmdstring)
    out_lines = out.split('\n')

    return returncode, out_lines


def get_ip():
    cmd = "/sbin/ifconfig | grep 'inet addr:' | grep -v '127.0.0.1' | awk  '{print $2}' | awk -F: '{print $2}'"

    returncode, ip_list = execute_command(cmd)

    return ip_list

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
            # print '%s   =====>   %s' % (dns, ip)
    return ip

def get_mysql_sock():
    cmd = "ls /tmp/mysql*"
    returncode, mysql_sock_list = execute_command(cmd)
    # print mysql_sock_list
    return mysql_sock_list


class mysql_sync:
    """mysql主备同步检测"""
    def __init__(self, unix_socket):
        self.unix_socket = unix_socket

        self.conn = MySQLdb.connect(user='root', passwd='dk76DSJ7DJA87da', unix_socket=unix_socket)
        self.cur = self.conn.cursor()

    def close(self):
         self.cur.close()
         self.conn.close()

    def show_master(self):
        self.cur.execute('show master status')
        result = self.cur.fetchone()
        (binlog_file, binlog_position, binlog_db) = result[0:3]
        # print (binlog_file, binlog_position, binlog_db)

        return (binlog_file, binlog_position, binlog_db)

    def show_slave(self):
        self.cur.execute('show slave status')
        result = self.cur.fetchone()

        if type(result) != type(None):
            Master_Host = result[1]
            Master_Port = result[3]
            Master_binlog_file = result[5]
            Master_binlog_position = result[6]
            Replicate_Do_DB = result[12]

            return (Master_Host, Master_Port, Master_binlog_file, Master_binlog_position, Replicate_Do_DB)

    def show_port(self):
        self.cur.execute("show variables like 'port'")
        result = self.cur.fetchone()
        port = result[1]

        return int(port)

    # 更新同步状态表
    def update_sync_table(self, dbName):
        sql = 'use %s;' % dbName
        self.cur.execute(sql)

        # 写入当前时间为同步状态
        curTime = today('%Y-%m-%d %H:%M:%S')
        ip_list = get_ip()

        # 判断同步状态表是否已新建
        num = self.cur.execute("show tables like 'sync_status'")
        if num == 0:
            sql = 'create table if not exists sync_status(ip varchar(32), curtime varchar(32));'
            self.cur.execute(sql)

        for ip in ip_list:
            sql = "update sync_status set curtime='%s' where ip='%s';" % (curTime, ip)
            num = self.cur.execute(sql)
            if num == 0:
                sql = "insert into sync_status(ip, curtime) values('%s', '%s');" % (ip, curTime)
                self.cur.execute(sql)

            self.conn.commit()

            # 最新状态写入文件
            fileName = '/home/maintainer/sync_status/%s.%s' % (ip, dbName)
            f = open(fileName, 'w')
            f.write(curTime)
            f.close()


    # 判断对端同步状态是否正常，不正常则重启同步
    def judgeSync(self, Master_Host, dbName):
        log.info('%9s判断与主机[%s]数据库[%s]的同步状态' % ('', Master_Host, dbName))

        sql = 'use %s;' % dbName
        self.cur.execute(sql)

        # 对端未开启监控，退出
        sql = "select curtime from sync_status where ip='%s' order by curtime desc limit 1" % (Master_Host)
        num = self.cur.execute(sql)
        if num == 0: return

        result = self.cur.fetchone()
        dbTime = result[0]

        fileName = '/home/maintainer/sync_status/%s.%s' % (Master_Host, dbName)
        f = open(fileName)
        fileTime = f.readline()
        f.close()


        # 计算写在数据库与写在文件时间差
        tmp_time1 = datetime.datetime.strptime(dbTime, '%Y-%m-%d %H:%M:%S')
        tmp_time2 = datetime.datetime.strptime(fileTime, '%Y-%m-%d %H:%M:%S')

        timeDelta = tmp_time2 - tmp_time1
        secondDelta = abs(timeDelta.days * 24 * 60 * 60 + timeDelta.seconds)

        # 时间差大于3分钟，重启同步
        if secondDelta > 180:
            log.info('%9s丢失同步状态:db[%s]file[%s], 时间差[%d]秒' % ('', dbTime, fileTime, secondDelta))
            self.cur.execute('stop slave;')
            self.cur.execute('start slave;')
        else:
            log.info('%9s同步状态正常:db[%s]file[%s], 时间差[%d]秒' % ('', dbTime, fileTime, secondDelta))


    # 清理一周前的同步状态数据
    def delData(self, dbName):

        # 当前时间
        curTime = today('%H:%M')
        if curTime == '01:01':
            log.info('开始清理数据库')
        else:
            return

        sql = 'use %s;' % dbName
        self.cur.execute(sql)

        delDate = dateCalc(today('%Y-%m-%d'), -7, fmt='%Y-%m-%d')
        ip_list = get_ip()
        for ip in ip_list:
            sql = "delete from sync_status where ip='%s' and curtime <= '%s'; " % (ip, delDate)
            self.cur.execute(sql)

            log.info('%9s开始清理数据库[%s]时间为[%s]前,ip为[%s]的数据' % ('', dbName, delDate, ip))

            self.conn.commit()


class NginxConf(object):
    """nginx配置文件读取"""
    def __init__(self, arg='/usr/local/nginx/conf/nginx.conf'):
        super(NginxConf, self).__init__()
        self.conf_file = arg

    def file2map(self, line_iter):
        """基于递归方法读取配置项"""
        pattLine = re.compile(r'(\w+)\s+(.+);')
        pattSub = re.compile(r'(.+)\{')

        conf_map = {}

        while True:
            try:
                line = line_iter.next()
            except StopIteration:
                break

            m = pattLine.match(line)
            m2 = pattSub.match(line)
            if m:
                key = m.group(1)
                value = m.group(2)
            elif m2:
                key = m2.group(1)
                value = self.file2map(line_iter)
            else:
                if line[0] == '}':
                    break

            # 如果值已存在，则追加新值
            if key in conf_map.keys():
                conf_map[key] = conf_map[key] + ' ' + value
            else:
                conf_map[key] = value

        return conf_map


    def read_item(self):
        """读取Nginx配置文件到Map"""
        fp = open(self.conf_file)

        lines = []
        new_line = True

        for line in fp.readlines():
            #跳过空行与注释
            line = line.split('#')[0]
            line = line.strip()
            if len(line) == 0: continue

            if line[-1] in (';', '{', '}'):
                if new_line:
                    lines.append(line)
                else:
                    tmp_line = lines[-1]
                    lines[-1] = tmp_line + line

                new_line = True
            else:
                if new_line:
                    lines.append(line)
                new_line = False

        fp.close()

        it = iter(lines)
        conf_map = self.file2map(it)

        return conf_map


class HostStatus(object):
    """主机状态"""
    def __init__(self):
        super(HostStatus, self).__init__()

    def heart(self):
        return today('%Y-%m-%d_%H:%M:%S')

    def host_ip(self):
        ip_list = get_ip()
        return ip_list[0]

    def nginx_site(self):
        site_path_map = {}

        conf = NginxConf()
        conf_map = conf.read_item()
        if 'http' in conf_map.keys():
            if 'server' in conf_map['http'].keys():
                server_map = conf_map['http']['server']
                site_path = server_map['root']
                server_name_list = server_map['server_name'].split(' ')
                site_path_map[site_path] = server_name_list

        conf_path = '/usr/local/nginx/conf/vhost'
        file_list = os.listdir(conf_path)
        # print file_list
        for file_name in file_list:
            ext_name_list = os.path.splitext(file_name)
            if ext_name_list[1] != '.conf': continue

            full_file_name = conf_path + '/' + file_name

            # print full_file_name
            conf = NginxConf(full_file_name)
            conf_map = conf.read_item()
            if 'server' in conf_map.keys():
                server_map = conf_map['server']
                # print server_map['server_name']
                # print server_map['root']
                site_path = server_map['root']
                server_name_list = server_map['server_name'].split(' ')
                if site_path in site_path_map.keys():
                    site_path_map[site_path].extend(server_name_list)
                else:
                    site_path_map[site_path] = server_name_list

        return site_path_map


    # 判断是否为PHP网站
    def is_php_site(self, path):
        db_conn_php_file = '%s/inc/config.inc.php' % path
        # print db_conn_php_file
        if not os.path.exists(db_conn_php_file):
            return False
        else:
            return True

    # 获取PHP网站连接的数据库端口与库名
    def site_db_param(self, path):
        db_conn_php_file = '%s/inc/config.inc.php' % path

        pattMySqlHost = re.compile(r'.*mysql_connect\("([a-zA-Z0-9\.:]+)",')
        pattMySqlDb = re.compile(r".*mysql_select_db\('(\w+)'\);")
        fp = open(db_conn_php_file)
        for line in fp.readlines():
            m1 = pattMySqlHost.match(line)
            m2 = pattMySqlDb.match(line)
            if m1:
                dbHost = m1.group(1)
            if m2:
                dbName = m2.group(1)
        fp.close()

        tmp_list = dbHost.split(":")
        host = tmp_list[0]
        if len(tmp_list) > 1:
            port = int(tmp_list[1])
        else:
            port = 3306

        return (port, dbName)


def main():
    sock_list = get_mysql_sock()

    hostStatus = HostStatus()
    log.info('当前主机:%s  运行监控脚本:%s' % (hostStatus.host_ip(), hostStatus.heart()))

    site_path_map = hostStatus.nginx_site()
    # print site_path_map
    log.info('找到Nginx服务:')
    for path, dns_list in site_path_map.items():
        log.info('   服务目录:%s' % (path))
        for dns in dns_list:
            if dns != 'www.lnmp.org':
                ip = dns2ip(dns)
            else:
                ip = hostStatus.host_ip()
                dns = ip

            log.info('      对应访问入口:%-20s IP:%s' % (dns, ip))

        if not hostStatus.is_php_site(path):
            log.info('      该服务是静态页面\n')
            continue

        # execute_command('echo "%s" >> /home/maintainer/all_host.txt' % (dns))

        port, dbName = hostStatus.site_db_param(path)
        log.info('      该服务是PHP网站，应对的数据库端口:%d  库名:%s' % (port, dbName))

        for sock in sock_list:
            mysql = mysql_sync(sock)

            if port == mysql.show_port():
                binlog_file, binlog_position, binlog_db = mysql.show_master()
                log.info('%9s数据库已开启binlog备份，当前为Master，备份参数:[%s][%s][%s]' %
                    ('', binlog_file, binlog_position, binlog_db))

                slaveStatusSet = mysql.show_slave()
                if type(slaveStatusSet) != type(None):
                    Master_Host, Master_Port, Master_binlog_file, Master_binlog_position, Replicate_Do_DB = slaveStatusSet
                    log.info('%9s数据库为备机Slave，其主服务器为:[%s][%s] ' % ('', Master_Host, Master_Port))
                    log.info('%13s备份库:[%s] 文件:[%s] 位置:[%s]\n' %
                        ('', Replicate_Do_DB, Master_binlog_file, Master_binlog_position))

                    mysql.update_sync_table(dbName)
                    log.info('%9s成功写入同步状态信息到数据库与文件中' % '')

                    mysql.judgeSync(Master_Host, dbName)

                # mysql.delData(dbName)
                break
            mysql.close()
        else:
            log.info('         该网站数据库端口:%d未开启\n' % port)


if __name__ == '__main__':
    main()
