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

user()
{
   local db=$1
   local sock=$2
   local pw=fafpo8f9ffFszfdhdaf
   #local pw=bfghj345gjdgFB#22K

   log "建立数据库与用户"

   mysql -S $sock -u$user -p$password << EOF
      FLUSH PRIVILEGES;

      create database $db;
      select user,host,password from mysql.user;

      create user '${db}'@'localhost' IDENTIFIED by '${pw}';

      grant all privileges on ${db}.* to ${db}@localhost;

      FLUSH PRIVILEGES;

EOF

   mysql -S $sock -u$db -p$pw $db << EOF
     show databases;
     show tables;

EOF
}

replication()
{
   local db=$1
   local sock=$2
   local pw=fafpo8f9ffFszfdhdaf

   log "建立数据库同步用户"

   mysql -S $sock -u$user -p$password << EOF

      grant replication slave on *.* to 'repl_user'@'59.188.133.54' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'59.188.133.55' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'103.250.15.58' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'103.250.15.59' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'103.250.12.58' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'103.250.12.59' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'112.213.126.135' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'112.213.126.136' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'112.213.126.137' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'103.250.15.202' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'103.247.165.156' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'103.247.165.157' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'103.20.195.125' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'210.245.214.162' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'210.245.214.163' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'43.243.51.40' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'43.243.51.41' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'210.245.214.230' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'210.245.214.231' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'59.188.43.8' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'59.188.43.9' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'210.245.214.198' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'210.245.214.199' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'103.250.15.66' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'103.250.15.67' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'103.17.116.37' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'103.17.116.38' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'103.17.116.39' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'210.245.214.244' identified by 'repl7hj&huu';
      grant replication slave on *.* to 'repl_user'@'210.245.214.245' identified by 'repl7hj&huu';

      FLUSH PRIVILEGES;

EOF
}

log "开始运行Mysql建库与用户"

#user dd0000 /tmp/mysql.sock
#replication dd5120 /tmp/mysql.sock

#replication dd5670 /tmp/mysql_3307.sock
#grant dd5670 /tmp/mysql_3307.sock

#user ddcscs /tmp/mysql_3308.sock
#                mysql_3308.sock

for i in "${!db[@]}"; do
    socket="/tmp/${sock[$i]}"
    log "$i" "${db[$i]}" "${host[$i]}" "$socket"

    #grant ${db[$i]} $socket
    replication ${db[$i]} $socket
done

log "运行Mysql建库与用户完成"

