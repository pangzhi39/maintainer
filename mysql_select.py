#!/usr/bin/python
#coding:gbk


import sys
import MySQLdb


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
        print (binlog_file, binlog_position, binlog_db)

        return (binlog_file, binlog_position, binlog_db)

    def show_slave(self):
        self.cur.execute('show slave status')
        result = self.cur.fetchone()
        Master_Host = result[1]
        Master_Port = result[3]
        Master_binlog_file = result[5]
        Master_binlog_position = result[6]
        Replicate_Do_DB = result[12]

        print (Master_Host, Master_Port, Master_binlog_file, Master_binlog_position, Replicate_Do_DB)
# try:
#     conn = MySQLdb.connect(user='root', passwd='dk76DSJ7DJA87da', unix_socket='/tmp/mysql.sock')
#     cur = conn.cursor()
#     cur.execute('show slave status')
#     result = cur.fetchone()
#     print result

#     cur.execute('show master status')
#     result = cur.fetchone()
#     print result

#     cur.close()
#     conn.close()

# except MySQLdb.Error, e:
#     print "Mysql Error %d: %s" % (e.args[0], e.args[1])


def main():
    mysql = mysql_sync('/tmp/mysql.sock')
    mysql.show_master()
    mysql.show_slave()
    mysql.close()


if __name__ == '__main__':
    main()