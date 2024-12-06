from days.day6.day6lib import R90R, Action, get_grid_and_start, is_loop, walk


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
        new_grid = grid.place_brick(pos)
        direction = first_visit_direction[pos]
        loop = is_loop(
            new_grid,
            pos - direction,
            R90R[direction],
        )
        if loop:
            brick_places.add(pos)
    return len(brick_places)


print(sol())
