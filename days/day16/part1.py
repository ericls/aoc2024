import math

from lib.input import get_input
from lib.path import Pt

UP = Pt(0, -1)
RIGHT = Pt(1, 0)
DOWN = Pt(0, 1)
LEFT = Pt(-1, 0)

R90R = {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}
R90L = {UP: LEFT, LEFT: DOWN, DOWN: RIGHT, RIGHT: UP}


from lib.measure import print_runtime


@print_runtime
def sol():
    input = get_input()
    grid = [list(row) for row in input.splitlines()]
    start = Pt(0, 0)
    end = Pt(0, 0)
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "S":
                start = Pt(x, y)
            if cell == "E":
                end = Pt(x, y)

    pos = start
    direction = RIGHT

    lowest_cost_from_start = {
        (start, RIGHT): 0,
    }

    queue = [(start, RIGHT)]
    while queue:
        pos, direction = queue.pop(0)
        cost = lowest_cost_from_start[(pos, direction)]
        for new_direction in [R90R[direction], R90L[direction]]:
            new_cost = cost + 1000
            if new_cost < lowest_cost_from_start.get((pos, new_direction), math.inf):
                lowest_cost_from_start[(pos, new_direction)] = new_cost
                queue.append((pos, new_direction))
        next_pos = pos + direction
        if grid[next_pos.y][next_pos.x] == "#":
            continue
        new_cost = cost + 1
        if new_cost < lowest_cost_from_start.get((next_pos, direction), math.inf):
            lowest_cost_from_start[(next_pos, direction)] = new_cost
            queue.append((next_pos, direction))

    return min(
        lowest_cost_from_start.get((end, UP), math.inf),
        lowest_cost_from_start.get((end, RIGHT), math.inf),
        lowest_cost_from_start.get((end, DOWN), math.inf),
        lowest_cost_from_start.get((end, LEFT), math.inf),
    )


print(sol())
