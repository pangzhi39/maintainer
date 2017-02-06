*/1 * * * * /usr/local/bin/python /home/maintainer/monitor.py
/home/backup/flush.sh
05 03 * * * /home/backup/flush.sh

* * * * * /home/backup/monitor.sh

*/10 * * * * /home/sync_mysql.sh >> /home/sync_mysql.log

00 03 * * * /home/maintainer/timer/backup_db.sh
02 14 * * * /home/maintainer/timer/revoke_db.sh
31 21 * * * /home/maintainer/timer/grant_db.sh

