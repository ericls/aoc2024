from bisect import bisect, insort
from collections import defaultdict
from dataclasses import dataclass

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
    bricks_index: tuple[dict[int, list[int]], dict[int, list[int]]]

    def place_brick(self, pos):
        by_x, by_y = self.bricks_index
        new_by_x = defaultdict(list)
        new_by_y = defaultdict(list)
        new_by_x.update({k: [*v] for k, v in by_x.items()})
        new_by_y.update({k: [*v] for k, v in by_y.items()})
        insort(new_by_x[pos.x], pos.y)
        insort(new_by_y[pos.y], pos.x)
        return Grid(
            self.width, self.height, set(self.bricks) | {pos}, (new_by_x, new_by_y)
        )


def build_bricks_index(bricks):
    by_x: dict[int, list[int]] = defaultdict(list)
    by_y: dict[int, list[int]] = defaultdict(list)
    for brick in bricks:
        insort(by_x[brick.x], brick.y)
        insort(by_y[brick.y], brick.x)
    return by_x, by_y


def next_brick(bricks_index, pos: Pt, direction: Pt):
    by_x, by_y = bricks_index

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
    return Grid(width, height, bricks, build_bricks_index(bricks)), start_pos


def in_bound(grid, pt):
    return 0 <= pt.x < grid.width and 0 <= pt.y < grid.width


def walk(grid: Grid, starting_pos, starting_direction=UP) -> list[tuple[Pt, Pt]]:
    current_pos = starting_pos
    current_direction = starting_direction
    path = [(current_pos, current_direction)]
    while True:
        next_pos = current_pos + current_direction
        if not in_bound(grid, next_pos):
            return path
        if next_pos in grid.bricks:
            current_direction = R90R[current_direction]
        else:
            current_pos = next_pos
            path.append((current_pos, current_direction))


def is_loop(grid: Grid, starting_pos, starting_direction):
    current_pos = starting_pos
    current_direction = starting_direction
    turns_set = set()

    while True:
        next_brick_pos = next_brick(grid.bricks_index, current_pos, current_direction)
        if next_brick_pos is None:
            return False
        current_pos = next_brick_pos - current_direction
        if (current_pos, current_direction) in turns_set:
            return True
        turns_set.add((current_pos, current_direction))
        current_direction = R90R[current_direction]
