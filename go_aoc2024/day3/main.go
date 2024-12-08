package main

import (
	_ "embed"
	"go_aoc2024/utils"
	"regexp"
	"strings"
)

//go:embed input.txt
var input string
var mul_regex = `mul\(\d+,\d+\)`
var do_regex = `do\(\)`
var dont_regex = `don't\(\)`

var all_regex = `(` + mul_regex + `|` + do_regex + `|` + dont_regex + `)`

func init() {
}

func eval_mul(s string) int {
	s = s[4:len(s)]
	s = strings.TrimPrefix(s, "(")
	s = strings.TrimSuffix(s, ")")
	parts := strings.Split(s, ",")
	a := utils.ParseInt(parts[0])
	b := utils.ParseInt(parts[1])
	return int(a * b)
}

func P1() int {
	s := 0
	r := regexp.MustCompile(mul_regex)
	for _, exp := range r.FindAllString(input, -1) {
		s += eval_mul(exp)
	}
	return s
}

func P2() int {
	s := 0
	r := regexp.MustCompile(all_regex)
	enabled := true
	for _, exp := range r.FindAllString(input, -1) {
		if exp == "do()" {
			enabled = true
		} else if exp == "don't()" {
			enabled = false
		} else if enabled {
			s += eval_mul(exp)
		}
	}
	return s
}

func main() {
	println("Part 1: ", P1())
	println("Part 2: ", P2())
}
