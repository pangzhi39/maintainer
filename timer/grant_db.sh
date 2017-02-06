#!/bin/sh

source /home/maintainer/timer/base_fun.sh

grant()
{
   bak_db=$1
   sock=$2

   log "开始授权mysql库: ${bak_db}"

   mysql -S $sock -u$user -p$password ${bak_db} << EOF

      grant all privileges on ${bak_db}.* to ${bak_db}@localhost;
      FLUSH PRIVILEGES;
EOF
}

log "开始运行Mysql授权脚本"

all()
{
for i in "${!db[@]}"; do
    socket="/tmp/${sock[$i]}"
    log "$i" "${db[$i]}" "${host[$i]}" "$socket"

    grant ${db[$i]} $socket
done
}

all
#grant ddcscs /tmp/mysql_3308.sock

log "运行Mysql授权脚本完成"

