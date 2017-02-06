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

ntpdate us.pool.ntp.org
date "+%Y-%m-%d %H:%M:%S"
