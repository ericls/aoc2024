package main

import (
	_ "embed"
	u "go_aoc2024/utils"
	"sort"
	"strings"
)

//go:embed input.txt
var input string

var leftList []int64
var rightList []int64

func init() {
	lines := strings.Split(strings.TrimSpace(input), "\n")
	for _, line := range lines {
		if line == "" {
			continue
		}
		a := strings.Fields(line)
		leftList = append(leftList, u.ParseInt(a[0]))
		sort.Slice(leftList, func(i, j int) bool {
			return leftList[i] < leftList[j]
		})
		rightList = append(rightList, u.ParseInt(a[1]))
		sort.Slice(rightList, func(i, j int) bool {
			return rightList[i] < rightList[j]
		})
	}
}

func P1() int64 {
	sum := int64(0)
	for pair := range u.Zip(leftList, rightList) {
		i, j := pair[0], pair[1]
		sum += u.Abs(i - j)
	}
	return sum
}

func P2() int64 {
	sum := int64(0)
	counts := u.Counter(rightList)
	for _, v := range leftList {
		sum += v * counts[v]
	}
	return sum
}

func main() {
	println("Part 1: ", P1())
	println("Part 2: ", P2())
}
