#!/bin/sh

#引用基础Shell函数库
source /home/maintainer/timer/base_fun.sh

log "=========" $curTime "============="

link_num=`netstat -an | grep ESTABLISHED | grep ":80" | wc -l`

log "link_num:" $link_num

cpu_io=`sar -u 1 1 | tail -n 1 | awk '{printf("%s,%s",$6,$8);}'`
mem=`sar -r 1 1 | tail -n 1 | awk '{printf("%s",$4);}'`

log "cpu  io :" $cpu_io "   mem:" $mem

nginx_count=`ps -ef | grep "nginx" | grep -v grep | wc -l`
php_count=`ps -ef | grep "php-fpm" | grep -v grep | wc -l`

log "nginx:" $nginx_count "php:" $php_count

mysql_pid=`ps -ef | grep mysqld | grep -v "mysqld_safe" | grep -v "grep" | awk '{print $2}'`

for pid in $mysql_pid; do
   mysql_thread=`pstree -p $pid | wc -l`
   log "mysql pid:" $pid "thread:" $mysql_thread
done

#ping_time=`ping 210.245.214.242 -s 1000 -c 6 | awk -F'=' '/time=/ {n++; sum+=$NF+0 } END{print sum/n}'`

#printf "time:%-10s web_line_num:%4s cpu_io:%s mem:%s nginx:%s php:%s mysql_pid:%s mysql_thread:%s\n" $curTime $link_num $cpu_io $mem $nginx_count $php_count $mysql_pid $mysql_thread

/home/maintainer/hostlist/ping.sh

#monfile=/home/backup/mondata/mon_data.$curDate


