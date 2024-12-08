package main

import (
	_ "embed"
	u "go_aoc2024/utils"
	"strings"
)

//go:embed input.txt
var input string

var int_list [][]int64

func init() {
	lines := strings.Split(strings.TrimSpace(input), "\n")
	for _, line := range lines {
		if line == "" {
			continue
		}
		var ints []int64
		for _, s := range strings.Fields(line) {
			ints = append(ints, u.ParseInt(s))
		}
		int_list = append(int_list, ints)
	}
}

func validateInts(ints []int64) bool {
	trend := 0
	for pair := range u.Pairwise(ints) {
		a, b := pair[0], pair[1]
		if u.Abs(a-b) > 3 || u.Abs(a-b) == 0 {
			return false
		}
		if a > b {
			if trend == 1 {
				return false
			}
			trend = -1
		} else if a < b {
			if trend == -1 {
				return false
			}
			trend = 1
		}
	}
	return true
}

func P1() int {
	count := 0
	for _, ints := range int_list {
		if validateInts(ints) {
			count++
		}
	}
	return count
}

func genInts(ints []int64) <-chan []int64 {
	out := make(chan []int64)
	go func() {
		out <- ints
		for i := range ints {
			newInts := make([]int64, 0, len(ints)-1)
			newInts = append(newInts, ints[:i]...)
			newInts = append(newInts, ints[i+1:]...)
			out <- newInts
		}
		close(out)
	}()
	return out
}

func P2() int {
	count := 0
	for _, ints := range int_list {
		for newInts := range genInts(ints) {
			if validateInts(newInts) {
				count++
				break
			}
		}
	}
	return count
}

func main() {
	println("Part 1: ", P1())
	println("Part 2: ", P2())
}
