#!/bin/sh

source /home/maintainer/timer/base_fun.sh

export_mysql()
{
   local db=$1
   local sock=$2

   log "停服务"
   service nginx stop

   log "锁表，停同步，查看同步BinLog位置"
   mysql -S $sock -u$user -p$password << EOF
      stop slave;
      FLUSH TABLES WITH READ LOCK;
      show master status;
EOF

   log "导出数据"
   mysqldump -S $sock --master-data -u$user -p$password $db > ${db}_${curDate}.sql 

   log "解表，启同步，查看同步BinLog位置"
   mysql -S $sock -u$user -p$password << EOF
      show master status;
      UNLOCK TABLES;
      start slave;
EOF

   log "启服务"
   service nginx start

   log "压缩数据"
   gzip ${db}_${curDate}.sql

}

import_mysql()
{
   local db=$1
   local sock=$2

   gunzip  ${db}_${curDate}.sql.gz

   mysql -S $sock -u$user -p$password $db < ${db}_${curDate}.sql

   log "查看同步BinLog位置"
   mysql -S $sock -u$user -p$password $db << EOF
      show master status;
EOF
}

log "开始运行Mysql导出数据脚本"

#export_mysql dd5670 /tmp/mysql_3306.sock
import_mysql dd5120 /tmp/mysql.sock

log "运行Mysql导出数据脚本完成"
