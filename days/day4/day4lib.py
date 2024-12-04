def str_for_path(grid, path):
    res = ""
    for x, y in path:
        if x < 0 or y < 0:
            return ""
        if y >= len(grid) or x >= len(grid[0]):
            return ""
        res += grid[y][x]
    return res


def four_letters_from(grid, x, y, dx, dy):
    path = []
    for i in range(4):
        path.append((x + dx * i, y + dy * i))
    return str_for_path(grid, path)


def count1(grid, x, y):
    c = 0
    for direction in [
        (1, 0),
        (0, 1),
        (1, 1),
        (-1, 1),
        (1, -1),
        (-1, -1),
        (0, -1),
        (-1, 0),
    ]:
        if four_letters_from(grid, x, y, *direction) == "XMAS":
            c += 1
    return c


def is_cross_mas(grid, x, y):
    line1 = [(x - 1, y - 1), (x, y), (x + 1, y + 1)]
    line2 = [(x + 1, y - 1), (x, y), (x - 1, y + 1)]

    line1_str = str_for_path(grid, line1)
    line2_str = str_for_path(grid, line2)

    if line1_str in ["MAS", "SAM"] and line2_str in ["MAS", "SAM"]:
        return 1
