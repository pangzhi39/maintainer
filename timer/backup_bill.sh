source /home/maintainer/timer/base_fun.sh

backup()
{
   bak_db=$1
   sock=$2
   table=$3

   log "��������mysql��: ${bak_db}.${table}"

   chmod 777 -R ${bak_dir}

   cd ${bak_dir}
   
   filename="${bak_db}_${table}_${curDate}.dat"

   if [ -f "$filename" ];then
      log "$filename file already exists"
   else
      mysqldump -S $sock -u$user -p$password -T /home/databak ${bak_db} ${table} 
      mv ${table}.txt ${filename}
      log "mysql�����ļ�: ${filename} ���ɳɹ�"
   fi
}

clean()
{
   bak_db=$1
   table=$2

   cd ${bak_dir}

   filename="${bak_db}_${table}_${fday}.dat"

   if [ -f $filename ];then
      rm -f $filename
      log "ɾ����5��ǰ�����ļ�:$filename ���"
   else
      log "׼��ɾ����5��ǰ�����ļ�:$filename ������"
   fi

}

log "��ʼ����Mysql���ݽű�"

for i in "${!db[@]}"; do
    socket="/tmp/${sock[$i]}"
    log "$i" "${db[$i]}" "${host[$i]}" "$socket"

    sleep 15
    backup ${db[$i]} $socket drop_bill
    backup ${db[$i]} $socket out_bill
    #backup ${db[$i]} $socket agent
    clean ${db[$i]} drop_bill
    clean ${db[$i]} out_bill
done

log "����Mysql���ݽű����"

