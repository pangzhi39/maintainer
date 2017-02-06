#!/bin/sh

source /home/maintainer/timer/base_fun.sh

update()
{
   bak_db=$1
   sock=$2

   mysql -S $sock -u$user -p$password ${bak_db} << EOF

      update ag_profit set profit_six = pre_profit_six
      where pre_profit_six <> 999;
      update ag_profit set profit2_six = pre_profit2_six
      where pre_profit2_six <> 999;
      update ag_profit set profit3_six = pre_profit3_six
      where pre_profit3_six <> 999;

      update ag_profit set pre_profit_six = 999
      where pre_profit_six <> 999;
      update ag_profit set pre_profit2_six = 999
      where pre_profit2_six <> 999;
      update ag_profit set pre_profit3_six = 999
      where pre_profit3_six <> 999;

      commit;
EOF
}

log "��ʼ����Mysql����ag_profit�ű�"

update  ddcscs "/tmp/mysql_3308.sock"

log "����Mysql����ag_profit�ű����"

