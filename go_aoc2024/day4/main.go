package main

import (
	_ "embed"
	"slices"
	"strings"
)

//go:embed input.txt
var input string
var lines []string

var directions8 = [8][2]int{
	{1, 0},
	{0, 1},
	{-1, 0},
	{0, -1},
	{1, 1},
	{-1, 1},
	{1, -1},
	{-1, -1},
}

var line1_d = [3][2]int{
	{-1, -1},
	{0, 0},
	{1, 1},
}

var line2_d = [3][2]int{
	{-1, 1},
	{0, 0},
	{1, -1},
}

func init() {
	lines = strings.Split(input, "\n")
}

func strOnPath(lines []string, path [][2]int) string {
	s := ""
	for _, p := range path {
		x, y := p[0], p[1]
		if x < 0 || y < 0 || x >= len(lines) || y >= len(lines[x]) {
			return ""
		}
		s += string(lines[y][x])
	}
	return s
}

func P1() int {
	s := 0
	for y, line := range lines {
		for x, c := range line {
			if c != 'X' {
				continue
			}
			for _, dir := range directions8 {
				path := [][2]int{}
				for i := 0; i < 4; i++ {
					path = append(path, [2]int{x + dir[0]*i, y + dir[1]*i})
				}
				str := strOnPath(lines, path)
				if str == "XMAS" {
					s += 1
				}
			}
		}
	}
	return s
}

func P2() int {
	s := 0
	targetStrs := []string{"MAS", "SAM"}
	for y, line := range lines {
		for x, _ := range line {
			line1 := [][2]int{}
			for _, d := range line1_d {
				line1 = append(line1, [2]int{x + d[0], y + d[1]})
			}
			str1 := strOnPath(lines, line1)
			line2 := [][2]int{}
			for _, d := range line2_d {
				line2 = append(line2, [2]int{x + d[0], y + d[1]})
			}
			str2 := strOnPath(lines, line2)
			if slices.Contains(targetStrs, str1) && slices.Contains(targetStrs, str2) {
				s += 1
			}
		}
	}
	return s
}

func main() {
	println("Part 1: ", P1())
	println("Part 2: ", P2())
}
