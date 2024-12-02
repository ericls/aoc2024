# courtesy of sciyoshi
import heapq
import math
from typing import Any, ClassVar, Dict, NamedTuple


class Pt(NamedTuple("Pt", [("x", int), ("y", int)])):
    N: ClassVar["Pt"]
    NE: ClassVar["Pt"]
    E: ClassVar["Pt"]
    SE: ClassVar["Pt"]
    S: ClassVar["Pt"]
    SW: ClassVar["Pt"]
    W: ClassVar["Pt"]
    NW: ClassVar["Pt"]

    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return type(self)(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return type(self)(self.x * other, self.y * other)

    def __div__(self, other):
        return type(self)(self.x / other, self.y / other)

    def __floordiv__(self, other):
        return type(self)(self.x // other, self.y // other)

    def __neg__(self):
        return type(self)(-self.x, -self.y)

    @property
    def rot90r(self):
        return type(self)(self.y, -self.x)

    @property
    def rot90l(self):
        return type(self)(-self.y, self.x)

    @property
    def norm1(self):
        return abs(self.x) + abs(self.y)

    @property
    def normi(self):
        return max(abs(self.x), abs(self.y))

    @property
    def norm2(self):
        return math.sqrt(self.x**2 + self.y**2)

    @property
    def nb4(self):
        return [self + d for d in [Pt.N, Pt.E, Pt.S, Pt.W]]

    @property
    def nb8(self):
        return [self + d for d in [Pt.N, Pt.NE, Pt.E, Pt.SE, Pt.S, Pt.SW, Pt.W, Pt.NW]]


Pt.N = Pt(0, 1)
Pt.NE = Pt(1, 1)
Pt.E = Pt(1, 0)
Pt.SE = Pt(1, -1)
Pt.S = Pt(0, -1)
Pt.SW = Pt(-1, -1)
Pt.W = Pt(-1, 0)
Pt.NW = Pt(-1, 1)


class Grd(Dict[Pt, Any]):
    def __init__(self, w=None, h=None):
        if w is not None and h is not None:
            for x in range(w):
                for y in range(h):
                    self[Pt(x, y)] = None

    def __str__(self):
        result = []
        for x in reversed(
            range(min(pt[0] for pt in self), max(pt[0] for pt in self) + 1)
        ):
            row = []
            for y in range(min(pt[1] for pt in self), max(pt[1] for pt in self) + 1):
                row.append(self[Pt(x, y)])
            result.append("".join(row))
        return "\n".join(result)

    def nb4(self, point: Pt):
        for pt in point.nb4:
            if pt in self:
                yield pt

    def nb8(self, point: Pt):
        for pt in point.nb8:
            if pt in self:
                yield pt


def astar_search(start, h_func, moves_func):
    # A priority queue, ordered by path length, f = g + h
    frontier = [(h_func(start), start)]
    # start state has no previous state; other states will
    previous = {start: None}
    # The cost of the best path to a state.
    path_cost = {start: 0}
    while frontier:
        (f, s) = heapq.heappop(frontier)
        if h_func(s) == 0:
            return Path(previous, s)
        for s2 in moves_func(s):
            new_cost = path_cost[s] + 1
            if s2 not in path_cost or new_cost < path_cost[s2]:
                heapq.heappush(frontier, (new_cost + h_func(s2), s2))
                path_cost[s2] = new_cost
                previous[s2] = s
    return dict(fail=True, front=len(frontier), prev=len(previous))


def Path(previous, s):
    return [] if (s is None) else Path(previous, previous[s]) + [s]
