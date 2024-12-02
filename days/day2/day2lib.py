from itertools import pairwise

from lib.input import get_input_lines


def get_ints():
    lines = get_input_lines()
    return [[int(x) for x in line.split()] for line in lines]


def produce_ints(ints):
    yield ints
    for i in range(len(ints)):
        yield ints[:i] + ints[i + 1 :]


def is_line_safe(ints):
    return all(1 <= abs(a - b) <= 3 for a, b in pairwise(ints)) and (
        all(a < b for a, b in pairwise(ints)) or all(a > b for a, b in pairwise(ints))
    )
