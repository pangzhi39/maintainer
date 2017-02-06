iplist=`cat /home/maintainer/hostlist/*.txt`
for ip in $iplist; do
  time=`ping $ip -s 1000 -c 6 | awk -F'=' '/time=/ {n++; sum+=$NF+0 } END{print sum/n}'`
  printf "IP=%-16s time=%sms\n" $ip $time
done
