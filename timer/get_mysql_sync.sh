#!/bin/sh

source /home/maintainer/timer/base_fun.sh

show_status()
{
   bak_db=$1
   sock=$2

   log "开始mysql库取同步状态: ${bak_db}"

   mysql -S $sock -u$user -p$password ${bak_db} << EOF

      show master status \G
      show slave status \G
EOF
}

log "开始运行Mysql取同步状态脚本"

for i in "${!db[@]}"; do
    socket="/tmp/${sock[$i]}"

    file=/home/maintainer/tmp/${db[$i]}.${host[$i]}
    show_status ${db[$i]} $socket > $file
    # grep "Master_Host:" $file
    masterip=`grep "Master_Host:" $file | cut -d ":" -f 2 | awk '{print substr($0,1,length($0)-1)}' `
    netstat -an | grep "$masterip" | grep ":330" | grep ESTABLISHED | grep -v "103.250.15.28:2049"
    cat $file
done

log "运行Mysql取同步状态脚本完成"

# for ip in `cat /home/maintainer/hostlist/*.txt`; do
#     iplist=""
# done

# netstat -an | egrep "(59.188.133.54|59.188.133.55)" | grep ":330" | grep ESTABLISHED | grep -v "103.250.15.28:2049"