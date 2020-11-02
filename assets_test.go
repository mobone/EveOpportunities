package main
import "C"
import (
 "sync"
)
var mtx sync.Mutex
//export Add
func Add(a, b int) int { return a + b }

func main() {}
// See awesome.go GitHub
