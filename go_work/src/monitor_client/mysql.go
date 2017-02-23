package main

import "fmt"
import "log"
import "database/sql"
import _ "github.com/go-sql-driver/mysql"

var db = &sql.DB{}

func init(){
    db,_ = sql.Open("mysql", "root:dk76DSJ7DJA87da@unix(/tmp/mysql.sock)/")
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

   return nil
}

func main() {
   Exec_sql("")
   fmt.Println("Hello")
}
