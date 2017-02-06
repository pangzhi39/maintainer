yum install -y ntp
yum install -y sysstat
yum install -y screen
yum install -y wget
yum install -y telnet
yum install -y crontabs
yum install -y MySQL-python

service crond start
service iptables stop
chkconfig iptables off
