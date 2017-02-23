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
    my_fun.ShellRun()

    ip_list := my_fun.Get_internal()
    for i := range ip_list {
       fmt.Printf("local[%s]\n", ip_list[i])
    }
}
 
