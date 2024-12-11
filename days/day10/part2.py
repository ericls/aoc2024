from collections import defaultdict
from days.day10.day10lib import build_grid
from lib.path import Pt


def build_path_count_map(grid):

    path_count_map: dict[Pt, int] = defaultdict(int)
    pt_by_num = defaultdict[int, list[Pt]](list)
    for y, row in enumerate(grid):
        for x, num in enumerate(row):
            pt = Pt(x, y)
            if num == 9:
                path_count_map[pt] = 1
            pt_by_num[num].append(pt)

    for i in range(8, -1, -1):
        for pt in pt_by_num[i]:
            for nb in pt.nb4:
                if 0 <= nb.x < len(grid[0]) and 0 <= nb.y < len(grid):
                    if grid[nb.y][nb.x] == i + 1:
                        path_count_map[pt] += path_count_map[nb]

    return path_count_map, pt_by_num


def sol():
    grid = build_grid()
    map_, pt_by_num = build_path_count_map(grid)
    c = 0
    for pt in pt_by_num[0]:
        c += map_[pt]

    return c


print(sol())
