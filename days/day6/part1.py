from days.day6.day6lib import Action, get_grid_and_start, walk


def sol():
    grid, start_pos = get_grid_and_start()
    actions, _ = walk(grid, start_pos)
    visited = set()
    for a, pt, _ in actions:
        if a == Action.VISIT:
            visited.add(pt)
    return len(visited)


print(sol())
