package monitor_common

type MysqlSyncStatus struct {
   Ip string
   Port string
   DB string
   LogFile string
   LogPos int64
}

type RequestMessage_mysql struct {
   ClientIp string
   Master MysqlSyncStatus
   Slave  MysqlSyncStatus
   SyncErrorMsg string
}

type ResponseMessage struct {
   ErrorCode string
   ErrorMsg  string
}

/* mysql状态表
CREATE TABLE mysql_status_detail(
   ID int unsigned not null  auto_increment,
   ClientIp varchar(32) not null,
   Master_Ip varchar(32),
   Master_Port varchar(32),
   Master_DB varchar(32),
   Master_LogFile varchar(64),
   Master_LogPos int(16) unsigned,
   Slave_Ip varchar(32),
   Slave_Port varchar(32),
   Slave_DB varchar(32),
   Slave_LogFile varchar(64),
   Slave_LogPos int(16) unsigned,
   SyncErrorMsg varchar(1024),
   primary key(ID)
);

*/