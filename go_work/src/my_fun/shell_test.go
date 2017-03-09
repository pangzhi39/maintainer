package my_fun

import (
   "fmt"
   "testing"
)
 
func TestShellRun(t *testing.T) {

   lines, err := ShellRun("netstat -an | grep 43.243.51.40 | grep ESTABLISHED | wc -l")
   if err != nil {
      //fmt.Println("Shell script error!", err.Error())
      t.Errorf("Shell script error:[%s]", err.Error())
      //return
   }
   for _, line := range lines {
    fmt.Printf("[%s]\n", line)
   }
}

func TestExternalIp(t *testing.T) {

   ip, err := Get_external()
   if err != nil {
      t.Errorf(err.Error())
   }
   fmt.Printf("External IP:[%s]\n", ip)
}

func TestHomeIp(t *testing.T) {

   homeIp, err := GetHomeIp()
   if err != nil {
      t.Errorf(err.Error())
   } else {
      fmt.Printf("HOME IP[%s]\n", homeIp)
   }
}

func TestInternalIp(t *testing.T) {

   ip_list := Get_internal()
   for _, ip := range ip_list {
      fmt.Printf("local IP[%s]\n", ip)
   }
}

func TestMysqlStatus(t *testing.T) {
   for ConnectNext() {
      // GetMasterStatus()
      row := QueryRow("show master status")
      fmt.Println(row)

      ret, err := CheckSlaveStatus()
      fmt.Println(ret)
      if err != nil {
         fmt.Println(err.Error())
      }
   }

}
