from enum import Enum, auto

from lib.input import get_input_lines
from lib.path import Pt

UP = Pt(0, -1)
RIGHT = Pt(1, 0)
DOWN = Pt(0, 1)
LEFT = Pt(-1, 0)

R90R = {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}


class Action(Enum):
    VISIT = auto()
    TURN = auto()


def get_grid_and_start():
    grid = get_input_lines()
    start_pos = Pt(0, 0)
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "^":
                start_pos = Pt(x, y)
    return grid, start_pos


def place_brick(grid, pos):
    new_grid = [row for row in grid]
    new_grid[pos.y] = new_grid[pos.y][: pos.x] + "#" + new_grid[pos.y][pos.x + 1 :]
    return new_grid


def in_bound(grid, pt):
    return 0 <= pt.x < len(grid[0]) and 0 <= pt.y < len(grid)


def walk(
    grid, starting_pos, starting_direction=UP, log_actions=True
) -> tuple[list[tuple[Action, Pt, Pt]], bool]:
    current_pos = starting_pos
    current_direction = starting_direction
    actions = [(Action.VISIT, current_pos, current_direction)]
    turn_sets = set()
    while True:
        next_pos = current_pos + current_direction
        if not in_bound(grid, next_pos):
            return actions, False
        if grid[next_pos.y][next_pos.x] == "#":
            current_direction = R90R[current_direction]
            if log_actions:
                actions.append((Action.TURN, current_pos, current_direction))
            if (current_pos, current_direction) in turn_sets:
                return actions, True
            turn_sets.add((current_pos, current_direction))
        else:
            current_pos = next_pos
            if log_actions:
                actions.append((Action.VISIT, current_pos, current_direction))
