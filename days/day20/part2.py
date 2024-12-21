from lib.input import get_input
from lib.measure import print_runtime
from lib.path import Pt

UP = Pt(0, -1)
RIGHT = Pt(1, 0)
DOWN = Pt(0, 1)
LEFT = Pt(-1, 0)


@print_runtime
def sol():
    input = get_input()
    grid = [list(line) for line in input.splitlines()]
    w, h = len(grid[0]), len(grid)
    start = Pt(0, 0)
    end = Pt(0, 0)
    bricks = set()

    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if char == "S":
                start = Pt(x, y)
            elif char == "E":
                end = Pt(x, y)
            elif char == "#":
                bricks.add(Pt(x, y))

    min_to_end = {end: 0}

    def inbound(pt: Pt):
        x, y = pt
        return 0 <= x < h and 0 <= y < w

    queue = [end]
    while queue:
        cur = queue.pop(0)
        for nb in cur.nb4:
            if not inbound(nb):
                continue
            if nb in bricks:
                continue
            new_cost = min_to_end[cur] + 1
            if new_cost < min_to_end.get(nb, new_cost + 1):
                min_to_end[nb] = new_cost
                queue.append(nb)

    path = [start]
    cur = start
    while cur != end:
        cur = min(cur.nb4, key=lambda nb: min_to_end.get(nb, float("inf")))
        path.append(cur)

    s = 0
    for i in range(0, len(path)):
        for j in range(len(path) - 1, i + 100, -1):
            posi = path[i]
            posj = path[j]
            dx = abs(posi.x - posj.x)
            if dx > 20:
                continue
            d = dx + abs(posi.y - posj.y)
            if d > 20:
                continue
            saved = j - i - d
            if saved >= 100:
                s += 1
    return s


print(sol())
