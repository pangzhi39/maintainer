package main
import (
   "fmt"
   "net/http"  
   "net/rpc"
   mc "monitor_common"
)

type Monitor int

func (t *Monitor) RecevieMysqlStatus (req *mc.RequestMessage_mysql, reply *mc.ResponseMessage) error {
   fmt.Println(req)

   return nil
}

func main() {
   monitor := new(Monitor)  
   rpc.Register(monitor)  
   rpc.HandleHTTP()  

   err := http.ListenAndServe("127.0.0.1:3234", nil)  
   if err != nil {  
      fmt.Println(err.Error())  
   }  
}
