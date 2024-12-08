package main

import (
	_ "embed"
	"go_aoc2024/utils"
	"slices"
	"strings"
)

//go:embed input.txt
var input string
var rules map[int64]([]int64)
var ints_list [][]int64

func init() {
	parts := strings.Split(input, "\n\n")
	rules_part, ints_part := parts[0], strings.TrimSpace(parts[1])
	rules = map[int64]([]int64){}
	rules_lines := strings.Split(rules_part, "\n")
	for _, line := range rules_lines {
		p := strings.Split(line, "|")
		a, b := utils.ParseInt(p[0]), utils.ParseInt(p[1])
		rules[a] = append(
			rules[a], b,
		)
	}
	ints_lines := strings.Split(ints_part, "\n")
	for _, line := range ints_lines {
		ints := utils.ParseInts(line, ",")
		ints_list = append(ints_list, ints)
	}
}

func validateInts(rules map[int64][]int64, ints []int64) bool {
	i := 0
	for i < len(ints)-1 {
		j := i + 1
		for j < len(ints) {
			a := ints[i]
			b := ints[j]
			if v, ok := rules[b]; ok {
				if slices.Contains(v, a) {
					return false
				}
			}
			j++
		}
		i++
	}
	return true
}

func sort(rules map[int64][]int64, ints []int64) []int64 {
	if len(ints) < 2 {
		return ints
	}
	a := ints[0]
	rest := ints[1:]
	afterA := []int64{}
	rule_a := rules[a]
	for _, b := range rest {
		if slices.Contains(rule_a, b) {
			afterA = append(afterA, b)
		}
	}
	beforeA := []int64{}
	for _, b := range rest {
		if !slices.Contains(afterA, b) {
			beforeA = append(beforeA, b)
		}
	}
	return append(
		append(sort(rules, beforeA), a),
		sort(rules, afterA)...,
	)
}

func P1() int64 {
	s := int64(0)
	for _, ints := range ints_list {
		if validateInts(rules, ints) {
			s += ints[len(ints)/2]
		}
	}
	return s
}

func P2() int64 {
	s := int64(0)
	for _, ints := range ints_list {
		if !validateInts(rules, ints) {
			sorted_ints := sort(rules, ints)
			s += sorted_ints[len(sorted_ints)/2]
		}
	}
	return s
}

func main() {
	println("Part 1: ", utils.MeasureRuntime(P1)())
	println("Part 2: ", utils.MeasureRuntime(P2)())
}
