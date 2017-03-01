package main
 
import (
   "my_fun"
   "fmt"
)
 
 
func main() {
 
    ip, err := my_fun.Get_external()
    if err != nil {
       fmt.Println(err)
    } else {
       fmt.Printf("[%s]\n", ip)
    }
    homeIp, err := my_fun.GetHomeIp()
    if err != nil {
       fmt.Println(err)
    } else {
       fmt.Printf("[%s]\n", homeIp)
    }

    lines, err := my_fun.ShellRun("netstat -an | grep 59.188.43.8 | grep :3306 | grep ESTABLISHED | wc -l")
    if err != nil {
       fmt.Println("Shell script error!", err.Error())
       return
    }
    for _, line := range lines {
       fmt.Printf("[%s]\n", line)
    }
    ip_list := my_fun.Get_internal()
    for i := range ip_list {
       fmt.Printf("local[%s]\n", ip_list[i])
    }
    return
}
 
