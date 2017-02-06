#!/bin/sh

source /home/maintainer/timer/base_fun.sh

backup()
{
   bak_db=$1
   sock=$2

   log "��������mysql��: ${bak_db}"

   cd ${bak_dir}
   
   if [ -f "${bak_db}_${curDate}.sql.gz" ];then
      log "${bak_db}_${curDate}.sql file already exists"
   else
      mysqldump -S $sock -u$user -p$password ${bak_db} | gzip > ${bak_db}_${curDate}.sql.gz
      log "mysql�����ļ�: ${bak_db}_${curDate}.sql.gz ���ɳɹ�"
   fi
}

clean()
{
   bak_db=$1

   cd ${bak_dir}

   filename="${bak_db}_${fday}.sql.gz"

   if [ -f $filename ];then
      rm -f $filename
      log "ɾ����5��ǰ�����ļ�:$filename ���"
   else
      log "׼��ɾ����5��ǰ�����ļ�:$filename ������"
   fi

   #��������ڸ�ʽ�ļ�
   old_fday=`date -d '5 days ago' +%y%m%d`
   filename="${bak_db}_${old_fday}.sql.gz"

   if [ -f $filename ];then
      rm -f $filename
      log "ɾ����5��ǰ�����ļ�:$filename ���"
   fi
}

log "��ʼ����Mysql���ݽű�"

socket="/tmp/mysql_3308.sock"
db=ddcscs

backup $db $socket
clean $db

log "����Mysql���ݽű����"

