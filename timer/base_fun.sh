curDate=`date +%Y%m%d`
curTime=`date +%H:%M:%S`

source /home/maintainer/timer/common_var.sh

logpath=/home/maintainer/timer/log               #��־Ŀ¼
logfile=$logpath/${host}.$curDate

#��־��¼���ļ�
log()
{
   exit_code=$?
   #logTime=`date "+%Y-%m-%d %H:%M:%S"`
   logTime=`date "+%H:%M:%S"`
   msg="$1 $2 $3 $4 $5 $6"
   execute=`basename $0`
   
   echo "$logTime $execute ����ID��$$  ����ֵ: $exit_code " >> $logfile
   echo "         $msg" >> $logfile

   echo "$msg"
}

#��־��¼���ļ�
log_host()
{
   local exit_code=$?
   local logTime=`date "+%Y-%m-%d %H:%M:%S"`
   #logTime=`date "+%H:%M:%S"`

   local file=$1 
   local fullfile=$logpath/${file}.log

   local msg="$2 $3 $4 $5 $6"
   local execute=`basename $0`
   
   echo "$logTime $execute ����ID��$$  ����ֵ: $exit_code " >> $fullfile
   echo "         $msg" >> $fullfile

   echo "$msg"
}

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/mysql/lib

export PATH=$PATH:$HOME/bin:/home/backup:/home/backup/bin:/usr/local/mysql/bin
