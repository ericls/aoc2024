from lib.input import get_input
from lib.measure import print_runtime
from lib.path import Pt


@print_runtime
def sol():
    input = get_input()
    width = 101
    height = 103
    ps = []
    vs = []
    for line in input.splitlines():
        line = line.removeprefix("p=")
        a, b = line.split(" v=")
        p = a.split(",")
        v = b.split(",")
        ps.append(Pt(int(p[0]), int(p[1])))
        vs.append(Pt(int(v[0]), int(v[1])))

    def wrap(pt):
        return Pt(pt.x % width, pt.y % height)

    def get_quad(p):
        if p.x == width // 2 or p.y == height // 2:
            return None
        if p.x < width // 2:
            if p.y < height // 2:
                return 1
            else:
                return 3
        else:
            if p.y < height // 2:
                return 2
            else:
                return 4

    after_move = []
    for p, v in zip(ps, vs):
        after_move.append(wrap(p + (v * 100)))

    quadrants = {1: [], 2: [], 3: [], 4: []}
    for p in after_move:
        q = get_quad(p)
        if q:
            quadrants[q].append(p)

    v = 1
    for a in quadrants.values():
        v *= len(a)

    return v


print(sol())
