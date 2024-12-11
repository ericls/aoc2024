from lib.input import get_input


def build_grid():
    input = get_input()
    lines = input.splitlines()
    grid = [[int(i) for i in line] for line in lines]
    return grid
