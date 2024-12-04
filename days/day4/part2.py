from days.day4.day4lib import is_cross_mas
from lib.input import get_input_lines


def sol():
    lines = get_input_lines()
    grid = lines
    count = 0
    for y, row in enumerate(grid):
        for x, _ in enumerate(row):
            if is_cross_mas(grid, x, y):
                count += 1

    return count


print(sol())
