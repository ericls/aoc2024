from collections import defaultdict

from days.day10.day10lib import build_grid
from lib.path import Pt


def build_reachable_map(grid):

    reachable_map = defaultdict(set[Pt])

    def get_reachable_9s(pt: Pt):
        if pt in reachable_map:
            return reachable_map[pt]
        num = grid[pt.y][pt.x]
        ret: set[Pt] = set()
        if num == 9:
            ret = set([pt])
        else:
            for nb in pt.nb4:
                if 0 <= nb.x < len(grid[0]) and 0 <= nb.y < len(grid):
                    if grid[nb.y][nb.x] == num + 1:
                        ret.update(get_reachable_9s(nb))
        reachable_map[pt] = ret
        return ret

    for y, row in enumerate(grid):
        for x, num in enumerate(row):
            pt = Pt(x, y)
            if num == 0:
                get_reachable_9s(pt)

    return reachable_map


def sol():
    grid = build_grid()
    map_ = build_reachable_map(grid)
    c = 0
    for y, row in enumerate(grid):
        for x, num in enumerate(row):
            pt = Pt(x, y)
            if num == 0:
                v = len(map_[pt])
                c += v

    return c


print(sol())
