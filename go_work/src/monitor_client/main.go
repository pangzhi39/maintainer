package main
 
import (
   "fmt"
   "strconv"
   "net/rpc"
   "my_fun"
   mc "monitor_common"
)
 
 
func main() {
 
   var reqMsg mc.RequestMessage_mysql
   // reply := new(mc.ResponseMessage)

   ip, err := my_fun.Get_external()
   if err != nil {
      fmt.Println(err)
   } else {
      // fmt.Printf("[%s]\n", ip)
      reqMsg.ClientIp = ip
      reqMsg.Master.Ip = ip
   }

   // 连接远程服务
   var reply mc.ResponseMessage
   client, err := rpc.DialHTTP("tcp", "127.0.0.1:3234")  
   if err != nil {  
      fmt.Println(err.Error())  
   }  
  

   // 枚举每个MySQL实例
   for my_fun.ConnectNext() {
      reqMsg.Master.Port = my_fun.Port
      
      // 读取主备的主节点状态
      row := my_fun.QueryRow("show master status")
      if row == nil {
         continue
      }
      // fmt.Println(row)

      reqMsg.Master.DB = row["Binlog_Do_DB"]
      reqMsg.Master.LogFile = row["File"]
      reqMsg.Master.LogPos, _ = strconv.ParseInt(row["Position"], 10, 0)

      ret, err := my_fun.CheckSlaveStatus()
      // fmt.Println(ret)

      reqMsg.Slave.Ip = ret.Master_Host
      reqMsg.Slave.Port = ret.Master_Port
      reqMsg.Slave.DB = ret.Db
      reqMsg.Slave.LogFile = ret.Master_Log_File
      reqMsg.Slave.LogPos = ret.Read_Master_Log_Pos
      if err != nil {
         fmt.Println(err.Error())
         reqMsg.SyncErrorMsg = err.Error()
      }

      err = client.Call("Monitor.RecevieMysqlStatus", &reqMsg, &reply)  
      if err != nil {  
         fmt.Println(err.Error())  
      } else {  
         fmt.Println(reply)  
      }  

      fmt.Println(reqMsg)
   }

   // 取RPC服务器IP，家里的
   homeIp, err := my_fun.GetHomeIp()
   if err != nil {
      fmt.Println(err)
   } else {
      fmt.Printf("[%s]\n", homeIp)
   }



   // return
}
 
