#!/bin/sh

source /home/maintainer/timer/base_fun.sh

revoke()
{
   bak_db=$1
   sock=$2

   log "开始权限回收mysql库: ${bak_db}"

   mysql -S $sock -u$user -p$password ${bak_db} << EOF

      revoke all privileges on ${bak_db}.* from ${bak_db}@localhost;
      GRANT select,insert,update,create,index ON ${bak_db}.* TO ${bak_db}@localhost;
      grant delete on ${bak_db}.ag_profit to ${bak_db}@localhost;
      grant delete on ${bak_db}.member_cut to ${bak_db}@localhost;
      grant delete on ${bak_db}.member_cut3d to ${bak_db}@localhost;
      grant delete on ${bak_db}.member_cutfjc to ${bak_db}@localhost;
      grant delete on ${bak_db}.member_cutgdc to ${bak_db}@localhost;
      grant delete on ${bak_db}.member_cutgxc to ${bak_db}@localhost;
      grant delete on ${bak_db}.member_cuthlj to ${bak_db}@localhost;
      grant delete on ${bak_db}.member_cutjxc to ${bak_db}@localhost;
      grant delete on ${bak_db}.member_cutkl8 to ${bak_db}@localhost;
      grant delete on ${bak_db}.member_cutpk10 to ${bak_db}@localhost;
      grant delete on ${bak_db}.member_cutpl3 to ${bak_db}@localhost;
      grant delete on ${bak_db}.member_cutssc to ${bak_db}@localhost;
      grant delete on ${bak_db}.member_cutssl to ${bak_db}@localhost;
      grant delete on ${bak_db}.member_cuttjc to ${bak_db}@localhost;
      grant delete on ${bak_db}.member_cuttjk to ${bak_db}@localhost;
      grant delete on ${bak_db}.member_cutxjc to ${bak_db}@localhost;
      grant delete on ${bak_db}.member_cutxyc to ${bak_db}@localhost;
      grant delete on ${bak_db}.online to ${bak_db}@localhost;
      grant delete on ${bak_db}.onuser to ${bak_db}@localhost;
      FLUSH PRIVILEGES;
EOF
}

log "开始运行Mysql权限回收脚本"

for i in "${!db[@]}"; do
    socket="/tmp/${sock[$i]}"
    log "$i" "${db[$i]}" "${host[$i]}" "$socket"

    revoke ${db[$i]} $socket
done

log "运行Mysql权限回收脚本完成"

