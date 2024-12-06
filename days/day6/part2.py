from days.day6.day6lib import R90R, Action, get_grid_and_start, place_brick, walk
from lib.path import Pt


def sol():
    grid, start_pos = get_grid_and_start()
    actions, _ = walk(grid, start_pos)

    first_visit_direction = {}
    for a, pt, direction in actions:
        if a == Action.VISIT:
            if pt not in first_visit_direction:
                first_visit_direction[pt] = direction

    brick_places = set()
    seen = set()
    for pos in first_visit_direction:
        if pos in seen:
            continue
        seen.add(pos)
        new_grid = place_brick(grid, pos)
        direction = first_visit_direction[pos]
        _, loop = walk(
            new_grid,
            pos - direction,
            R90R[direction],
            log_actions=False,
        )
        if loop:
            brick_places.add(pos)
    return len(brick_places)


print(sol())
