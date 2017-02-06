#!/bin/sh

source /home/maintainer/timer/base_fun.sh

restart_slave()
{
   port=$1

   log "开始重启同步服务mysql库: ${port}"
   # log "mysql -h 127.0.0.1 --port=$port -u$user -p$password"
   mysql -h 127.0.0.1 --port=$port -u$user -p$password << EOF
      stop slave;
      start slave;
EOF
}

case $1 in
  up)     # 开机时间
    date -d "$(awk -F. '{print $1}' /proc/uptime) second ago" +"%Y-%m-%d %H:%M:%S"
    ;;
  up_h)     # 开机时间
    date -d "$(awk -F. '{print $1}' /proc/uptime) second ago" +"%Y%m%d%H%M%S|%Y-%m-%d %H:%M:%S"
    ;;
  resync)     # 重启同步
    restart_slave $2
    ;;
  *)
    echo "未知命令"
    exit -1
    ;;
esac
