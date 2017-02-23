package main

import (
   "fmt"
   "os"
)

type point struct {
   x, y int
}

func main() {
   p := point{1, 2}

   // {1 2}
   fmt.Printf("%v\n", p)

   // {x:1 y:2}
   fmt.Printf("%+v\n", p)

   // main.point{x:1, y:2}
   fmt.Printf("%#v\n", p)

   // main.point
   fmt.Printf("%T\n", p)

   // true
   fmt.Printf("%t\n", true)

   fmt.Printf("%d\n", 123)
   fmt.Printf("%b\n", 14)
   fmt.Printf("%c\n", 33)
   fmt.Printf("%x\n", 456)

   fmt.Printf("%f\n", 78.9)

   fmt.Printf("%e\n", 123400000.0)
   fmt.Printf("%E\n", 123400000.0)

   // "String"
   fmt.Printf("%s\n", "\"String\"")

   // "\"String\""
   fmt.Printf("%q\n", "\"String\"")

   fmt.Printf("%t\n", true)

   fmt.Fprintf(os.Stderr, "an %s\n", "error")
}
