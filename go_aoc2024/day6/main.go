package main

import (
	_ "embed"
	"go_aoc2024/utils"
	"sort"
	"strings"
)

//go:embed input.txt
var input string
var initGrid Grid
var startPos Pt

func init() {
	lines := strings.Split(input, "\n")
	for y, line := range lines {
		for x, c := range line {
			if c == '^' {
				startPos = Pt{X: x, Y: y}
			}
		}
	}
	initGrid = newGrid(lines)
}

type Pt = utils.Pt

type PtDirection struct {
	pt        Pt
	direction Pt
}

var UP = Pt{X: 0, Y: -1}
var DOWN = Pt{X: 0, Y: 1}
var LEFT = Pt{X: -1, Y: 0}
var RIGHT = Pt{X: 1, Y: 0}

var R90R = map[Pt]Pt{
	UP:    RIGHT,
	RIGHT: DOWN,
	DOWN:  LEFT,
	LEFT:  UP,
}

type BrickIndex struct {
	byX map[int][]int
	byY map[int][]int
}

type Grid struct {
	width       int
	height      int
	bricks      map[Pt]bool
	bricksIndex *BrickIndex
}

func insort(a []int, x int) []int {
	i := sort.SearchInts(a, x)
	if i < len(a) && a[i] == x {
		return a
	}
	a = append(a, 0)
	copy(a[i+1:], a[i:])
	a[i] = x
	return a
}

func buildBricksIndex(bricks map[Pt]bool) *BrickIndex {
	byX := map[int][]int{}
	byY := map[int][]int{}
	for pt := range bricks {
		byX[pt.X] = insort(byX[pt.X], pt.Y)
		byY[pt.Y] = insort(byY[pt.Y], pt.X)
	}
	return &BrickIndex{byX, byY}
}

func newGrid(lines []string) Grid {
	bricks := map[Pt]bool{}
	for y, line := range lines {
		for x, c := range line {
			if c == '#' {
				bricks[Pt{X: x, Y: y}] = true
			}
		}
	}
	return Grid{
		len(lines[0]),
		len(lines),
		bricks,
		buildBricksIndex(bricks),
	}
}

func (bi *BrickIndex) withNewBrick(pt Pt) *BrickIndex {
	byX := map[int][]int{}
	byY := map[int][]int{}
	for x, ys := range bi.byX {
		byX[x] = append(byX[x], ys...)
	}
	for y, xs := range bi.byY {
		byY[y] = append([]int{}, xs...)
	}
	byX[pt.X] = insort(byX[pt.X], pt.Y)
	byY[pt.Y] = insort(byY[pt.Y], pt.X)
	return &BrickIndex{byX, byY}
}

func (bi *BrickIndex) nextBrick(pos Pt, direction Pt) *Pt {
	if direction == UP {
		x := pos.X
		index := sort.SearchInts(bi.byX[x], pos.Y)
		if index > 0 {
			return &Pt{X: x, Y: bi.byX[x][index-1]}
		}
	} else if direction == DOWN {
		x := pos.X
		index := sort.SearchInts(bi.byX[x], pos.Y)
		if index < len(bi.byX[x]) {
			return &Pt{X: x, Y: bi.byX[x][index]}
		}
	} else if direction == LEFT {
		y := pos.Y
		index := sort.SearchInts(bi.byY[y], pos.X)
		if index > 0 {
			return &Pt{X: bi.byY[y][index-1], Y: y}
		}
	} else if direction == RIGHT {
		y := pos.Y
		index := sort.SearchInts(bi.byY[y], pos.X)
		if index < len(bi.byY[y]) {
			return &Pt{X: bi.byY[y][index], Y: y}
		}
	}
	return nil
}

func (g *Grid) withNewBrick(pt Pt) Grid {
	bricks := map[Pt]bool{}
	for k, v := range g.bricks {
		bricks[k] = v
	}
	bricks[pt] = true
	return Grid{
		g.width,
		g.height,
		bricks,
		g.bricksIndex.withNewBrick(pt),
	}
}

func (g *Grid) isOutOfBound(pos Pt) bool {
	if pos.X < 0 || pos.Y < 0 || pos.X >= g.width-1 || pos.Y >= g.height-1 {
		return true
	}
	return false
}

func walk(grid Grid, pos Pt, direction Pt) []PtDirection {
	path := []PtDirection{}
	for {
		path = append(path, PtDirection{pos, direction})
		maybeNextPos := pos.Add(direction)
		if grid.isOutOfBound(maybeNextPos) {
			break
		}
		if grid.bricks[maybeNextPos] {
			direction = R90R[direction]
			continue
		}
		pos = maybeNextPos
	}
	return path
}

func isLoop(grid Grid, pos Pt, direction Pt) bool {
	seenTurns := map[PtDirection]bool{}
	for {
		nextBrick := grid.bricksIndex.nextBrick(pos, direction)
		if nextBrick == nil {
			return false
		}
		pos = nextBrick.Sub(direction)
		if seenTurns[PtDirection{pos, direction}] {
			return true
		}
		seenTurns[PtDirection{pos, direction}] = true
		direction = R90R[direction]
	}
}

func P1() int {
	path := walk(initGrid, startPos, UP)
	uniquePos := map[Pt]bool{}
	for _, pos := range path {
		uniquePos[pos.pt] = true
	}
	return len(uniquePos)
}

func P2() int {
	s := 0
	path := walk(initGrid, startPos, UP)
	firstPosDirection := map[Pt]Pt{}
	for _, pos := range path {
		if _, ok := firstPosDirection[pos.pt]; ok {
			continue
		}
		firstPosDirection[pos.pt] = pos.direction
	}
	for pos, direction := range firstPosDirection {
		newGrid := initGrid.withNewBrick(pos)
		if isLoop(newGrid, pos.Sub(direction), R90R[direction]) {
			s += 1
		}
	}
	return s
}

func main() {
	println("Part 1: ", utils.MeasureRuntime(P1)())
	println("Part 2: ", utils.MeasureRuntime(P2)())
}
