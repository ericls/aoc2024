from days.day6.day6lib import get_grid_and_start, walk


def sol():
    grid, start_pos = get_grid_and_start()
    path = walk(grid, start_pos)
    visited = set()
    for pt, _ in path:
        visited.add(pt)
    return len(visited)


print(sol())
