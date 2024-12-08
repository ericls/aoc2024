package main

import (
	_ "embed"
	"go_aoc2024/utils"
	"strings"
)

//go:embed input.txt
var input string

var equations []Equation

type Equation struct {
	Target int64
	Ints   []int64
}

func init() {
	lines := strings.Split(strings.TrimSpace(input), "\n")
	for _, line := range lines {
		if line == "" {
			continue
		}
		a := strings.Split(line, ": ")
		target := utils.ParseInt(a[0])
		ints := utils.ParseInts(a[1], " ")
		equations = append(equations, Equation{Target: target, Ints: ints})
	}
}

func Add(a, b int64) int64 {
	return a + b
}

func Mul(a, b int64) int64 {
	return a * b
}

func Concat(a, b int64) int64 {
	for _, scale := range []int64{10, 100, 1000} {
		if b < scale {
			return a*scale + b
		}
	}
	panic("Concat: b too large")
}

func (eq Equation) validate(ops []func(a, b int64) int64) bool {
	var inner func(head int64, i int) bool
	inner = func(head int64, i int) bool {
		if i == len(eq.Ints) {
			return head == eq.Target
		}
		next := eq.Ints[i]
		for _, op := range ops {
			if inner(op(head, next), i+1) {
				return true
			}
		}
		return false
	}
	return inner(eq.Ints[0], 1)
}

func P1() int64 {
	var sum int64
	for _, eq := range equations {
		if eq.validate([]func(a, b int64) int64{Add, Mul}) {
			sum += eq.Target
		}
	}
	return sum
}

func P2() int64 {
	var sum int64
	for _, eq := range equations {
		if eq.validate([]func(a, b int64) int64{Add, Mul, Concat}) {
			sum += eq.Target
		}
	}
	return sum
}

func main() {
	println("Part 1: ", utils.MeasureRuntime(P1)())
	println("Part 2: ", utils.MeasureRuntime(P2)())
}
