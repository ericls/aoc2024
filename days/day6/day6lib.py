from bisect import bisect, insort
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, auto
from functools import cached_property

from lib.input import get_input_lines
from lib.path import Pt

UP = Pt(0, -1)
RIGHT = Pt(1, 0)
DOWN = Pt(0, 1)
LEFT = Pt(-1, 0)

R90R = {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}


@dataclass
class Grid:
    width: int
    height: int
    bricks: set[Pt]

    def place_brick(self, pos):
        return Grid(self.width, self.height, set(self.bricks) | {pos})

    @cached_property
    def indexed_bricks(self):
        by_x: dict[int, list[int]] = defaultdict(list)
        by_y: dict[int, list[int]] = defaultdict(list)
        for brick in self.bricks:
            insort(by_x[brick.x], brick.y)
            insort(by_y[brick.y], brick.x)
        return by_x, by_y

    def next_brick(self, pos: Pt, direction: Pt):
        by_x, by_y = self.indexed_bricks

        if direction == UP:
            x = pos.x
            index = bisect(by_x[x], pos.y)
            if index > 0:
                return Pt(x, by_x[x][index - 1])
            return None
        if direction == DOWN:
            x = pos.x
            index = bisect(by_x[x], pos.y)
            if index < len(by_x[x]):
                return Pt(x, by_x[x][index])
            return None
        if direction == LEFT:
            y = pos.y
            index = bisect(by_y[y], pos.x)
            if index > 0:
                return Pt(by_y[y][index - 1], y)
            return None
        if direction == RIGHT:
            y = pos.y
            index = bisect(by_y[y], pos.x)
            if index < len(by_y[y]):
                return Pt(by_y[y][index], y)
            return None


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
    width = len(grid[0])
    height = len(grid)
    bricks = set()
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "#":
                bricks.add(Pt(x, y))
    return Grid(width, height, bricks), start_pos


def in_bound(grid, pt):
    return 0 <= pt.x < grid.width and 0 <= pt.y < grid.width


def walk(
    grid: Grid, starting_pos, starting_direction=UP, log_actions=True
) -> tuple[list[tuple[Action, Pt, Pt]], bool]:
    current_pos = starting_pos
    current_direction = starting_direction
    actions = [(Action.VISIT, current_pos, current_direction)]
    turn_sets = set()
    while True:
        next_pos = current_pos + current_direction
        if not in_bound(grid, next_pos):
            return actions, False
        if next_pos in grid.bricks:
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


def is_loop(grid: Grid, starting_pos, starting_direction):
    current_pos = starting_pos
    current_direction = starting_direction
    turns_set = set()

    while True:
        next_turn_pos = grid.next_brick(current_pos, current_direction)
        if next_turn_pos is None:
            return False
        current_pos = next_turn_pos - current_direction
        if (current_pos, current_direction) in turns_set:
            return True
        turns_set.add((current_pos, current_direction))
        current_direction = R90R[current_direction]
