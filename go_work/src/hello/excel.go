package main

import (
    "github.com/tealeg/xlsx"
)

func main() {
    file := xlsx.NewFile()
    sheet,_ := file.AddSheet("Sheet9")
    row := sheet.AddRow()
    row.SetHeightCM(1)
    cell := row.AddCell()
    cell.Value = "haha"
    cell = row.AddCell()
    cell.Value = "xixi"

    err := file.Save("file.xlsx")
    if err != nil {
        panic(err)
    }

}
