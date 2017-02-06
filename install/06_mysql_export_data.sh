#!/bin/sh

source /home/maintainer/timer/base_fun.sh

export_mysql()
{
   local db=$1
   local sock=$2

   log "ͣ����"
   service nginx stop

   log "����ͣͬ�����鿴ͬ��BinLogλ��"
   mysql -S $sock -u$user -p$password << EOF
      stop slave;
      FLUSH TABLES WITH READ LOCK;
      show master status;
EOF

   log "��������"
   mysqldump -S $sock --master-data -u$user -p$password $db > ${db}_${curDate}.sql 

   log "�����ͬ�����鿴ͬ��BinLogλ��"
   mysql -S $sock -u$user -p$password << EOF
      show master status;
      UNLOCK TABLES;
      start slave;
EOF

   log "������"
   service nginx start

   log "ѹ������"
   gzip ${db}_${curDate}.sql

}

import_mysql()
{
   local db=$1
   local sock=$2

   gunzip  ${db}_${curDate}.sql.gz

   mysql -S $sock -u$user -p$password $db < ${db}_${curDate}.sql

   log "�鿴ͬ��BinLogλ��"
   mysql -S $sock -u$user -p$password $db << EOF
      show master status;
EOF
}

log "��ʼ����Mysql�������ݽű�"

#export_mysql dd5670 /tmp/mysql_3306.sock
import_mysql dd5120 /tmp/mysql.sock

log "����Mysql�������ݽű����"
