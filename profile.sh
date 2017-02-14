#/bin/sh

set -o vi

export LANG=zh_CN.gbk

alias cdn="cd /usr/local/nginx/conf"
alias cdm="cd /usr/local/mysql"
alias cdp="cd /usr/local/php/etc"
alias cdw="cd /home/wwwroot"
alias cdmt="cd /home/maintainer"
alias mysql3307="mysql -S /tmp/mysql_3307.sock"
alias mysql3308="mysql -S /tmp/mysql_3308.sock"

alias ll="ls -rtlh"

set TMOUT=0

export PATH=./:$PATH:/home/maintainer:/usr/local/mysql/bin

week=`date +%W`
ntpFile=/tmp/${week}.st

if [ ! -f $ntpFile ]; then
   ntpdate us.pool.ntp.org
   date "+%Y-%m-%d %H:%M:%S"
   touch $ntpFile
fi

alias g1m="ssh 'root@59.188.43.8'"
alias g1s="ssh 'root@103.250.15.58'"
alias g2m="ssh 'root@112.213.126.135'"
alias g2s="ssh 'root@43.243.51.40'"
alias g4m="ssh 'root@103.20.195.60'"
alias g5m="ssh 'root@210.245.214.162'"
alias g6m="ssh 'root@210.245.214.198'"
alias g6s="ssh 'root@103.250.15.66'"

ssh_all_run()
{
   cmd=$1
   g1m $cmd
   g1s $cmd
   g2m $cmd
   g4m $cmd
   g5m $cmd
   g6m $cmd
   g6s $cmd
}

alias all_test="ssh_all_run 'cd /home/maintainer/; ls -rtlh'"
alias all_update="ssh_all_run 'cd /home/maintainer/; git pull origin master'"
