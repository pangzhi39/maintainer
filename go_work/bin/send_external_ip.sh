#!/bin/sh

ip=`/home/maintainer/go_work/bin/external_ip`
if [ $? -eq 0 ]; then
   #echo $ip
   /usr/bin/ssh root@103.250.15.58 "echo $ip > /home/wwwroot/default_dd3840/ip.txt"
fi
