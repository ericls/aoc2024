from days.day6.day6lib import R90R, get_grid_and_start, is_loop, walk


def sol():
    grid, start_pos = get_grid_and_start()
    path = walk(grid, start_pos)

    first_visit_direction = {}
    for pt, direction in path:
        if pt not in first_visit_direction:
            first_visit_direction[pt] = direction

    c = 0
    for pos in first_visit_direction:
        new_grid = grid.place_brick(pos)
        direction = first_visit_direction[pos]
        if is_loop(
            new_grid,
            pos - direction,
            R90R[direction],
        ):
            c += 1
    return c


print(sol())
