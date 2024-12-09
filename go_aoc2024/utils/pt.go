package utils

import "strconv"

type Pt struct {
	X, Y int
}

func (p Pt) Add(q Pt) Pt {
	return Pt{p.X + q.X, p.Y + q.Y}
}

func (p Pt) Sub(q Pt) Pt {
	return Pt{p.X - q.X, p.Y - q.Y}
}

func (p Pt) String() string {
	return "Pt(" + strconv.Itoa(p.X) + ", " + strconv.Itoa(p.Y) + ")"
}

func MakePt(x, y int) Pt {
	return Pt{x, y}
}
