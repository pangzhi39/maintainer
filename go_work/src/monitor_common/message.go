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
