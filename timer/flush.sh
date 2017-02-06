#!/bin/sh

#Shell

source /home/backup/base_fun.sh

monfile=/home/backup/flush.log

echo "=======================================" >> $monfile
echo $curTime >> $monfile
free -g  >> $monfile
sync
echo 3 > /proc/sys/vm/drop_caches
free -g  >> $monfile
echo 0 > /proc/sys/vm/drop_caches

