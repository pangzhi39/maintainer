#!/bin/sh

source /home/maintainer/timer/base_fun.sh

restart_slave()
{
   port=$1

   log "��ʼ����ͬ������mysql��: ${port}"
   # log "mysql -h 127.0.0.1 --port=$port -u$user -p$password"
   mysql -h 127.0.0.1 --port=$port -u$user -p$password << EOF
      stop slave;
      start slave;
EOF
}

case $1 in
  up)     # ����ʱ��
    date -d "$(awk -F. '{print $1}' /proc/uptime) second ago" +"%Y-%m-%d %H:%M:%S"
    ;;
  up_h)     # ����ʱ��
    date -d "$(awk -F. '{print $1}' /proc/uptime) second ago" +"%Y%m%d%H%M%S|%Y-%m-%d %H:%M:%S"
    ;;
  resync)     # ����ͬ��
    restart_slave $2
    ;;
  *)
    echo "δ֪����"
    exit -1
    ;;
esac
