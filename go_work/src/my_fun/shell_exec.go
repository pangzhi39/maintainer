package my_fun

import (
    "fmt"
    "io/ioutil"
    "os/exec"
//    "time"
)
 
func ShellRun() {
    fmt.Println("1111111111111")

    cmd := exec.Command("/bin/sh", "-c", "who -r | awk '{print $3,$4}'")
    stdout, err := cmd.StdoutPipe()
    if err != nil {
        fmt.Println("StdoutPipe: " + err.Error())
        return
    }
 
    stderr, err := cmd.StderrPipe()
    if err != nil {
        fmt.Println("StderrPipe: ", err.Error())
        return
    }
 
    if err := cmd.Start(); err != nil {
        fmt.Println("Start: ", err.Error())
        return
    }
 
    bytesErr, err := ioutil.ReadAll(stderr)
    if err != nil {
        fmt.Println("ReadAll stderr: ", err.Error())
        return
    }
 
    if len(bytesErr) != 0 {
        fmt.Printf("stderr is not nil: %s", bytesErr)
        return
    }
 
    bytes, err := ioutil.ReadAll(stdout)
    if err != nil {
        fmt.Println("ReadAll stdout: ", err.Error())
        return
    }
 
    if err := cmd.Wait(); err != nil {
        fmt.Println("Wait: ", err.Error())
        return
    }
 
    fmt.Printf("stdout: %s", bytes)
}
 