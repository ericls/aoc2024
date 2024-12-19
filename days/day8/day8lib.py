from collections import defaultdict
from itertools import permutations

from lib.input import get_input_lines
from lib.path import Pt


def get_map():
    lines = get_input_lines()
    width = len(lines[0])
    height = len(lines)

    map_ = defaultdict(list)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == ".":
                continue
            map_[c].append(Pt(x, y))

    return (width, height), map_


def inbound(pos, width, height):
    x, y = pos
    return 0 <= x < width and 0 <= y < height


def gen_locations_1(ant_locations, width, height):
    for a, b in permutations(ant_locations, 2):
        diff = b - a
        loc = b + diff
        if inbound(loc, width, height):
            yield loc


def gen_locations_2(ant_locations, width, height):
    for a, b in permutations(ant_locations, 2):
        diff = b - a
        yield a
        yield b
        loc = b + diff
        while inbound(loc, width, height):
            yield loc
            loc = loc + diff


def count_locations(gen, map_, width, height):
    seen = set()
    for v in map_.values():
        seen.update(gen(v, width, height))
    return len(seen)
