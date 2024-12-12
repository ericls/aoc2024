from bisect import insort
from collections import defaultdict
from dataclasses import dataclass
from itertools import pairwise
from typing import NamedTuple

from lib.path import Pt

UP = Pt(0, -1)
RIGHT = Pt(1, 0)
DOWN = Pt(0, 1)
LEFT = Pt(-1, 0)


class Boarder(NamedTuple):
    from_: Pt
    norm: Pt


class Grid:

    def __init__(self, data: list[list[str]]) -> None:
        self.data = data

    def inbound(self, pt):
        x, y = pt.x, pt.y
        return 0 <= x < len(self.data[0]) and 0 <= y < len(self.data)

    def get_value(self, pt):
        if self.inbound(pt):
            return self.data[pt.y][pt.x]
        return None


def count_int_gaps(ints: list[int]) -> int:
    return len([p for p in pairwise(ints) if p[1] - p[0] > 1])


@dataclass
class Area:

    def __init__(self, grid: Grid) -> None:
        self.grid = grid
        self.pts = set[Pt]()

    def add_pt(self, pt: Pt):
        self.pts.add(pt)

    @property
    def all_boarders(self):
        sides = set[Boarder]()
        for pt in self.pts:
            pt_value = self.grid.get_value(pt)
            for direction in [UP, RIGHT, DOWN, LEFT]:
                nb = pt + direction
                nb_value = self.grid.get_value(nb)
                if pt_value != nb_value:
                    sides.add(Boarder(pt, direction))
        return sides

    @property
    def perimeter(self):
        return len(self.all_boarders)

    @property
    def sides(self):
        v_sides: dict[tuple[int, Pt], list[int]] = defaultdict(list)
        h_sides: dict[tuple[int, Pt], list[int]] = defaultdict(list)

        for side in self.all_boarders:
            if side.norm in [LEFT, RIGHT]:
                key = (side.from_.x, side.norm)
                insort(v_sides[key], side.from_.y)
            elif side.norm in [UP, DOWN]:
                key = (side.from_.y, side.norm)
                insort(h_sides[key], side.from_.x)

        num_sides = 0
        for ints in v_sides.values():
            num_sides += count_int_gaps(ints) + 1
        for ints in h_sides.values():
            num_sides += count_int_gaps(ints) + 1

        res = num_sides
        return res

    @property
    def fence_cost(self):
        return len(self.pts) * self.perimeter

    @property
    def bulk_cost(self):
        return len(self.pts) * self.sides

    @classmethod
    def build_areas(cls, grid: Grid):
        area_map: dict[Pt, Area] = {}
        areas = []

        def set_area(pt, area=None):
            if pt in area_map:
                return
            if area is None:
                area = Area(grid)
                areas.append(area)
            area_map[pt] = area
            area_map[pt].add_pt(pt)
            c = grid.get_value(pt)
            for nb in pt.nb4:
                v = grid.get_value(nb)
                if v == c:
                    set_area(nb, area)

        for y, row in enumerate(grid.data):
            for x in range(len(row)):
                pt = Pt(x, y)
                set_area(pt)

        return areas
