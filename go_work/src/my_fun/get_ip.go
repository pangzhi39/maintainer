package my_fun
 
import (
    s "strings"
    // "flag"
    // "fmt"
    "net"
    "io/ioutil"
    "net/http"
    // "os"
)
 
// var get_ip = flag.String("get_ip", "", "external|internal")
 
// func main() {
//     fmt.Println("Usage of ./getmyip --get_ip=(external|internal)")
//     flag.Parse()
//     if *get_ip == "external" {
//         Get_external()
//     }
 
//     if *get_ip == "internal" {
//         Get_internal()
//     }
 
 
// }
 
func Get_external() (string, error){
    resp, err := http.Get("http://myexternalip.com/raw")
    if err != nil {
        return "", err
    }
    defer resp.Body.Close()
   
    ipByte, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        return "", err
    }

    return s.Replace(string(ipByte), "\n", "", -1), nil
}

func Get_internal() []string{
    addrs, err := net.InterfaceAddrs()
    if err != nil {
        panic(err)
    }
    ip_list := make([]string, 0, 10)

    for _, a := range addrs {
        if ipnet, ok := a.(*net.IPNet); ok && !ipnet.IP.IsLoopback() {
            if ipnet.IP.To4() != nil {
                // os.Stdout.WriteString(ipnet.IP.String() + "\n")
                ip_list = append(ip_list, ipnet.IP.String())
            }
        }
    }

    return ip_list
}

func GetHomeIp() (string, error){
    resp, err := http.Get("http://103.250.15.58/ip.txt")
    if err != nil {
        return "", err
    }
    defer resp.Body.Close()
   
    ipByte, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        return "", err
    }

    return s.Replace(string(ipByte), "\n", "", -1), nil
}