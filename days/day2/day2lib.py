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
    trend = None
    for a, b in pairwise(ints):
        if abs(a - b) < 1 or abs(a - b) > 3:
            return False
        if b > a:
            if trend == -1:
                return False
            trend = 1
        elif b < a:
            if trend == 1:
                return False
            trend = -1
    return True
