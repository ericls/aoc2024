from days.day4.day4lib import count1
from lib.input import get_input_lines


def sol():
    lines = get_input_lines()
    grid = lines

    counts = 0

    for y, row in enumerate(grid):
        for x, _ in enumerate(row):
            counts += count1(grid, x, y)

    return counts


print(sol())
