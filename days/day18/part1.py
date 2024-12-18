import re
from itertools import batched

from lib.input import get_input
from lib.path import Pt

UP = Pt(0, -1)
RIGHT = Pt(1, 0)
DOWN = Pt(0, 1)
LEFT = Pt(-1, 0)


from lib.measure import print_runtime


@print_runtime
def sol():
    input = get_input()
    h, w = 71, 71
    ints = map(int, re.findall(r"\d+", input))
    start = Pt(0, 0)
    end = Pt(h - 1, w - 1)
    bricks = [Pt(x, y) for x, y in batched(ints, 2)]
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
            new_cost = min_to_end[cur] + 1
            if new_cost < min_to_end.get(nb, new_cost + 1):
                min_to_end[nb] = new_cost
                queue.append(nb)

    added_bricks = set()

    def add_brick(pos: Pt):
        added_bricks.add(pos)
        if pos not in min_to_end:
            return
        invalidate_queue = [pos]
        refill_queue = []
        while invalidate_queue:
            cur = invalidate_queue.pop(0)
            if cur not in min_to_end:
                continue
            cur_value = min_to_end[cur]
            del min_to_end[cur]
            for nb in cur.nb4:
                if not inbound(nb):
                    continue
                if nb not in min_to_end:
                    continue
                if min_to_end[nb] < cur_value:
                    continue

                invalid_nb = True
                for nbnb in nb.nb4:
                    if nbnb == cur:
                        continue
                    if min_to_end.get(nbnb, cur_value + 1) <= cur_value:
                        invalid_nb = False
                        break
                if invalid_nb:
                    invalidate_queue.insert(0, nb)
                else:
                    refill_queue.append(nb)

        while refill_queue:
            cur = refill_queue.pop(0)
            if cur not in min_to_end:
                continue
            for nb in cur.nb4:
                if not inbound(nb):
                    continue
                if nb in added_bricks:
                    continue
                new_cost = min_to_end[cur] + 1
                if new_cost < min_to_end.get(nb, new_cost + 1):
                    min_to_end[nb] = new_cost
                    refill_queue.append(nb)

    for brick in bricks[:1024]:
        add_brick(brick)

    return min_to_end[start]


print(sol())
