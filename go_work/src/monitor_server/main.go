package main
import (
   "fmt"
   "log"
   "net/http"  
   "net/rpc"
   mc "monitor_common"
   "database/sql"
   _ "github.com/go-sql-driver/mysql"
)

const (
   dbUser = "root"
   dbPassword = "lscprm02"
   sock_file = "/var/run/mysqld/mysqld.sock"
)
func init() {
   connect_str := fmt.Sprintf("%s:%s@unix(%s)/monitor", dbUser, dbPassword, sock_file)
   db, _ = sql.Open("mysql", connect_str)
   
}

var db = &sql.DB{}

// 对外提供服务
type Monitor int

func (t *Monitor) RecevieMysqlStatus (req *mc.RequestMessage_mysql, reply *mc.ResponseMessage) error {
   fmt.Println(*req)
   Insert(req)

   reply.ErrorCode = "0"
   reply.ErrorMsg = "交易成功"
   return nil
}

func Insert(req *mc.RequestMessage_mysql) {
   str_sql := ` INSERT INTO mysql_status_detail(
      ClientIp,
      Master_Ip, Master_Port, Master_DB, Master_LogFile, Master_LogPos,
      Slave_Ip, Slave_Port, Slave_DB, Slave_LogFile, Slave_LogPos,
      SyncErrorMsg, TS)
      VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, now())`

   stmt, err := db.Prepare(str_sql)
   if err != nil {
       log.Fatal(err)
   }
   defer stmt.Close()

   _, err = stmt.Exec(req.ClientIp, req.Master.Ip, req.Master.Port, req.Master.DB, req.Master.LogFile, req.Master.LogPos,
      req.Slave.Ip, req.Slave.Port, req.Slave.DB, req.Slave.LogFile, req.Slave.LogPos, req.SyncErrorMsg)
   if err != nil {
       log.Fatal(err)
   }
   // lastId, err := res.LastInsertId()
   // if err != nil {
   //     log.Fatal(err)
   // }
   // rowCnt, err := res.RowsAffected()
   // if err != nil {
   //     log.Fatal(err)
   // }
   // log.Printf("ID = %d, affected = %d\n", lastId, rowCnt)
} 

func Listen() {
   monitor := new(Monitor)  
   rpc.Register(monitor)  
   rpc.HandleHTTP()  

   err := http.ListenAndServe("0.0.0.0:9000", nil)  
   if err != nil {  
      fmt.Println(err.Error())  
   }
}

func main() {
   Listen()
}