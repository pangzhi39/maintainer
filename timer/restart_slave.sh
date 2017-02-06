#!/bin/bash

source /home/maintainer/timer/base_fun.sh

restart_slave()
{
   bak_db=$1
   sock=$2

   log "��ʼ����ͬ������mysql��: ${bak_db}"

   mysql -S $sock -u$user -p$password ${bak_db} << EOF

      stop slave;
      start slave;
EOF
}

log "��ʼ����Mysql��������ͬ������"

for i in "${!db[@]}"; do
    socket="/tmp/${sock[$i]}"
    log "$i" "${db[$i]}" "${host[$i]}" "$socket"

    restart_slave ${db[$i]} $socket
done

log "����Mysql��������ͬ���������"

