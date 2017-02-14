#!/usr/bin/env bash

netstat -an | grep '80 103.250.15.58:22' | grep ESTABLISHED | awk '{print $5}' | grep -oP '\d+\.\d+\.\d+\.\d+' > /home/wwwroot/default_dd3840/ip.txt

#*/30 * * * * /usr/bin/ssh root@103.250.15.58 "/home/maintainer/monitor/wzh_ip.sh"
#who am i | grep -oP '\d+\.\d+\.\d+\.\d+' > /home/wwwroot/default_dd3840/ip.txt
