#!/bin/sh

source /home/maintainer/timer/base_fun.sh

backup()
{
   bak_db=$1
   sock=$2

   log "开户备份mysql库: ${bak_db}"

   cd ${bak_dir}
   
   if [ -f "${bak_db}_${curDate}.sql.gz" ];then
      log "${bak_db}_${curDate}.sql file already exists"
   else
      mysqldump -S $sock -u$user -p$password ${bak_db} | gzip > ${bak_db}_${curDate}.sql.gz
      log "mysql备份文件: ${bak_db}_${curDate}.sql.gz 生成成功"
   fi
}

clean()
{
   bak_db=$1

   cd ${bak_dir}

   filename="${bak_db}_${fday}.sql.gz"

   if [ -f $filename ];then
      rm -f $filename
      log "删除的5天前数据文件:$filename 完成"
   else
      log "准备删除的5天前数据文件:$filename 不存在"
   fi

   #清理旧日期格式文件
   old_fday=`date -d '5 days ago' +%y%m%d`
   filename="${bak_db}_${old_fday}.sql.gz"

   if [ -f $filename ];then
      rm -f $filename
      log "删除的5天前数据文件:$filename 完成"
   fi
}

log "开始运行Mysql备份脚本"

socket="/tmp/mysql_3308.sock"
db=ddcscs

backup $db $socket
clean $db

log "运行Mysql备份脚本完成"

