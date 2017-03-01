package my_fun

import (
   "fmt"
   "log"
   "time"
   "errors"
   "database/sql"
   "strconv"
   // s "strings"
   _ "github.com/go-sql-driver/mysql"
)

type MysqlSalveStatus struct {
   Db, Master_Host string
   Master_Port int
   Master_Log_File string 
   Read_Master_Log_Pos int64
}

const (
   dbUser = "root"
   dbPassword = "dk76DSJ7DJA87da"
)

var db = &sql.DB{}

// Socket连接文件列表
var Sock_file_list []string
var Port string
var curDbIdx int = 0

func init(){
   cmd := fmt.Sprintf("ls /tmp/mysql*.sock")
   lines, err := ShellRun(cmd)
   if err != nil {
      panic(err)
   }

   Sock_file_list = lines

   // for _, sock_file := range Sock_file_list {
   //    fmt.Printf("[%s]\n", sock_file)
   // }

   // fmt.Println(len(Sock_file_list))
   if len(Sock_file_list) == 1 {
      Connect(Sock_file_list[0])
   }
} 

// 按Scoket文件连接数据库
func Connect(sock_file string) error{
   connect_str := fmt.Sprintf("%s:%s@unix(%s)/", dbUser, dbPassword, sock_file)
   db, _ = sql.Open("mysql", connect_str)

   row := QueryRow("show global variables like 'port'")
   // fmt.Printf("[%s]\n", row["Value"])
   Port = row["Value"]

   return nil
}

// 连接当前数值对应的数据库
func ConnectNext() bool {
   if curDbIdx < len(Sock_file_list) {
      Connect(Sock_file_list[curDbIdx])
      curDbIdx ++
      return true
   }
   return false
}

func Exec_sql(sql string) error {
   rows, _ := db.Query("show databases")
   defer rows.Close()

   for rows.Next() {
      var dbname string
      if err := rows.Scan(&dbname); err != nil {
            log.Fatal(err)
      }
      fmt.Println(dbname)
   }

   result, _ := db.Exec("use dd3840")
   fmt.Println(result)

   rows2, _ := db.Query("show tables")
   defer rows2.Close()

   for rows2.Next() {
      var table_name string
      if err := rows2.Scan(&table_name); err != nil {
            log.Fatal(err)
      }
      fmt.Println(table_name)
   }

   return nil
}

func GetMasterStatus() {
   row := db.QueryRow("show master status")

   var file, position, dbname, ignoreDb string
   err := row.Scan(&file, &position, &dbname, &ignoreDb)
   if err != nil {
      panic(err)
   }

   fmt.Println("file, position, dbname")
   fmt.Println(file, position, dbname)
}

func CheckSlaveStatus() (MysqlSalveStatus, error) {
   row := QueryRow("show slave status")

   var status MysqlSalveStatus
   status.Db = row["Replicate_Do_DB"]
   status.Master_Host = row["Master_Host"]
   status.Master_Port, _ = strconv.Atoi(row["Master_Port"])
   status.Master_Log_File = row["Master_Log_File"]
   status.Read_Master_Log_Pos, _ = strconv.ParseInt(row["Read_Master_Log_Pos"], 10, 0)

   // 检查IO与SQL运行状态
   if row["Slave_IO_Running"] != "Yes" {
      return status, errors.New("Slave_IO_Running Error")
   }
   if row["Slave_SQL_Running"] != "Yes" {
      return status, errors.New("Slave_SQL_Running Error")
   }

   // 检查网络连接状态
   cmd := fmt.Sprintf("netstat -an | grep %s | grep ESTABLISHED | wc -l", row["Master_Host"])
   lines, err := ShellRun(cmd)
   if err != nil {
      panic(err)
   }

   // 连接数判断
   connectNum, _ := strconv.Atoi(lines[0])
   if connectNum < 2 {
      return status, errors.New("netstat 连接数少于2 Error")
   }

   return status, nil
}

func printValue(pval *interface{}) string {
    var s_txt string
    switch v := (*pval).(type) {
    case nil:
        s_txt = "NULL"
    case time.Time:
        s_txt = "'" + v.Format("2006-01-02 15:04:05.999") + "'"
    case int, int8, int16, int32, int64, float32, float64, byte:
        s_txt = fmt.Sprint(v)
    case []byte:
        s_txt = string(v)
    case bool:
        if v {
            s_txt = "'1'"
        } else {
            s_txt = "'0'"
        }
    default:
        s_txt = "'" + fmt.Sprint(v) + "'"
    }
    return s_txt
}

func Query(sql_stmt string) (map[int]map[string]string) {

   // result, _ := db.Exec("use mysql")
   // fmt.Println(result)

   //查询数据库
   query, err := db.Query(sql_stmt)
   if err != nil {
      fmt.Println("查询数据库失败", err.Error())
      panic(err.Error())
   }
   defer query.Close()

   //读出查询出的列字段名
   cols, _ := query.Columns()
   //values是每个列的值，这里获取到byte里
   values := make([]sql.RawBytes, len(cols))
   //query.Scan的参数，因为每次查询出来的列是不定长的，用len(cols)定住当次查询的长度
   scanArgs := make([]interface{}, len(cols))
   //让每一行数据都填充到[][]byte里面
   for i := range values {
      scanArgs[i] = &values[i]
   }

   //最后得到的map
   results := make(map[int]map[string]string)
   i := 0
   for query.Next() { //循环，让游标往下推
      //query.Scan查询出来的不定长值放到scanArgs[i] = &values[i],也就是每行都放在values里
      if err := query.Scan(scanArgs...); err != nil { 
         fmt.Println(err)
         panic(err.Error())
      }

      row := make(map[string]string) //每行数据

      for k, v := range values { //每行数据是放在values里面，现在把它挪到row里
         key := cols[k]
         row[key] = string(v)
      }
      results[i] = row //装入结果集中
      i ++
   }

   // 查询出来的数组
   // for k, v := range results {
   //    fmt.Println(k, v)
   // }

   return results
}

func QueryRow(sql_stmt string) (map[string]string) {
   //查询数据库
   ds := Query(sql_stmt)
   
   // 查询出来的数组
   // for k, v := range ds {
   //    fmt.Println(k, v)
   // }

   if len(ds) >= 1 {
      return ds[0]
   }else {
      return nil
   }
}

func mysql_test() {
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
