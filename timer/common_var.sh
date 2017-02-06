
bak_dir=/home/databak
fday=`date -d '5 days ago' +%Y%m%d`

user=root
password=dk76DSJ7DJA87da
sock=(mysql.sock)

case $HOSTNAME in
  S210245214232)     # 54 组1主
    host=(g1_master_54)
    db=(dd3840)
    ;;
  S210245214246)     # 246 组1_replace主
    host=(g1_master_246)
    db=(dd3840)
    ;;

  S103250152829)     #28 组1备 组4备
    host=(g1_slave_28 g4_slave_28)
    db=(dd3840 dd8989)
    sock=(mysql.sock mysql_3307.sock)
    ;;

  localhost)     # 组2主 112.213.126.135
    host=(g2_master_135)
    db=(dd5670)
    ;;

  S59188133121122)   #156 组3主 
    host=(g3_master_156)
    db=(dd5120)
    ;;

  localhost.localdomain)   #125 组4主 
    host=(g4_master_125)
    db=(dd8989)
    ;;

  P210245214242243)   #242 组5主 
    host=(g5_master_242)
    db=(dd3855)
    ;;

  S43243512425)   #40 组2备 组5备
    host=(g5_slave_40 g2_slave_40)
    db=(dd3855 dd5670)
    sock=(mysql.sock mysql_3307.sock mysql_3308.sock)
    ;;

  s210245214165)   # 组6主
    host=(g6_master_176)
    db=(dd5120)
    sock=(mysql.sock)
    ;;

  S10325015196)   # 组6备
    host=(g6_slave_66)
    db=(dd5120)
    sock=(mysql.sock)
    ;;
  *)
    echo "未定义主机"
    exit -1
    ;;
esac

#for i in "${!db[@]}"; do 
#    socket="/tmp/${sock[$i]}"
#    printf "%s\t%s\t%s\t%s\n" "$i" "${db[$i]}" "${host[$i]}" "$socket"
#done
