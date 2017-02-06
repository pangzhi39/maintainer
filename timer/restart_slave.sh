#!/bin/bash

source /home/maintainer/timer/base_fun.sh

restart_slave()
{
   bak_db=$1
   sock=$2

   log "开始重启同步服务mysql库: ${bak_db}"

   mysql -S $sock -u$user -p$password ${bak_db} << EOF

      stop slave;
      start slave;
EOF
}

log "开始运行Mysql重启主从同步服务"

for i in "${!db[@]}"; do
    socket="/tmp/${sock[$i]}"
    log "$i" "${db[$i]}" "${host[$i]}" "$socket"

    restart_slave ${db[$i]} $socket
done

log "运行Mysql重启主从同步服务完成"

