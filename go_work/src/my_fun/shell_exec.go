package my_fun

import (
    "fmt"
    "io/ioutil"
    "os/exec"
    "errors"
    s "strings"
//    "time"
)
 
// 运行Shell命令，并返回字符串数据
func ShellRun(cmd_stmt string) ([]string, error) {

    //cmd := exec.Command("/bin/sh", "-c", "who -r | awk '{print $3,$4}'")
    cmd := exec.Command("/bin/sh", "-c", cmd_stmt)
    stdout, err := cmd.StdoutPipe()
    if err != nil {
        //fmt.Println("StdoutPipe: " + err.Error())
        //return
        panic(err)
    }
 
    stderr, err := cmd.StderrPipe()
    if err != nil {
        //fmt.Println("StderrPipe: ", err.Error())
        //return
        panic(err)
    }
 
    if err := cmd.Start(); err != nil {
        //fmt.Println("Start: ", err.Error())
        //return
        panic(err)
    }
 
    bytesErr, err := ioutil.ReadAll(stderr)
    if err != nil {
        //fmt.Println("ReadAll stderr: ", err.Error())
        //return
        panic(err)
    }
 
    if len(bytesErr) != 0 {
        errMsg := fmt.Sprintf("cmd:[%s] stderr:[%s]", cmd_stmt, bytesErr)
        panic(errors.New(errMsg))
    }
 
    bytes, err := ioutil.ReadAll(stdout)
    if err != nil {
        //fmt.Println("ReadAll stdout: ", err.Error())
        //return
        panic(err)
    }
 
    if err := cmd.Wait(); err != nil {
        errMsg := fmt.Sprintf("cmd:[%s] Error:[%s]", cmd_stmt, err.Error())
        // fmt.Println("Wait: ", err.Error())
        return nil, errors.New(errMsg)
        // panic(err)
    }
 
    lines := s.Split(s.TrimSpace(string(bytes)), "\n")

    ret_lines := make([]string, len(lines))
    for i, line := range lines {
       ret_lines[i] = s.TrimSpace(line)
   }
    // fmt.Printf("[%s][%q][%x]\n", bytes, bytes, bytes)
    // lines := s.Split(string(bytes), "\n")
    // for _, line := range lines {
    //     fmt.Println(line) 
    // }
    return ret_lines, nil
}
 
