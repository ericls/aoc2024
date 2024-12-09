package main

import (
	_ "embed"
	"go_aoc2024/utils"
	"strings"
)

//go:embed input.txt
var input string

type Antenna struct {
	position utils.Pt
	freq     string
}

type Grid struct {
	Width    int
	Height   int
	antennas map[string][]Antenna
}

func (g *Grid) inbound(pos *utils.Pt) bool {
	return 0 <= pos.X && pos.X < g.Width && 0 <= pos.Y && pos.Y < g.Height
}

var grid Grid

func init() {
	lines := strings.Split(strings.TrimSpace(input), "\n")
	grid.Width = len(lines[0])
	grid.Height = len(lines)
	grid.antennas = make(map[string][]Antenna)
	for y, line := range lines {
		for x, c := range line {
			if c != '.' {
				grid.antennas[string(c)] = append(
					grid.antennas[string(c)],
					Antenna{position: utils.Pt{X: x, Y: y}, freq: string(c)},
				)
			}
		}
	}
}

func P1() int {
	seen := make(map[utils.Pt]bool)
	for _, antennas := range grid.antennas {
		for pair := range utils.Permutation2(antennas) {
			a, b := pair[0].position, pair[1].position
			diff := b.Sub(a)
			pos := b.Add(diff)
			if grid.inbound(&pos) {
				seen[pos] = true
			}
		}
	}
	return len(seen)
}

func P2() int {
	seen := make(map[utils.Pt]bool)
	for _, antennas := range grid.antennas {
		for pair := range utils.Permutation2(antennas) {
			a, b := pair[0].position, pair[1].position
			diff := b.Sub(a)
			seen[a] = true
			seen[b] = true
			for {
				pos := b.Add(diff)
				if !grid.inbound(&pos) {
					break
				}
				seen[pos] = true
				b = pos
			}
		}
	}
	return len(seen)
}

func main() {
	println("Part 1: ", utils.MeasureRuntime(P1)())
	println("Part 2: ", utils.MeasureRuntime(P2)())
}
