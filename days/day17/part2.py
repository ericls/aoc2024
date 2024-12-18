import re

from days.day17.day17lib import Machine, run
from lib.input import get_input


def sol():
    input = get_input()
    digits = map(int, re.findall(r"\d+", input))
    _, _, _, *program = digits

    def get_possible_numbers(target):
        possible = []
        for i in range(0, 1 << (7 + 3)):
            n = Machine(i, 0, 0, program).next()
            if n == target:
                possible.append(i)
        return possible

    d_maps = {i: get_possible_numbers(i) for i in range(8)}

    def search(target, last_7_bits=None):
        res = []
        for d in d_maps[target]:
            if last_7_bits is None:
                res.append(d)
            elif d % 0b10000000 == last_7_bits:
                res.append(d)
        return res

    def fill_bits(selected, rem: list[int]):
        if not rem:
            return [selected]
        target = rem[0]
        if selected:
            last_7 = (selected[-1] >> 3) % 0b10000000
        else:
            last_7 = None
        possible_next = search(target, last_7)
        res = []
        for p in possible_next:
            r = fill_bits(selected + [p], rem[1:])
            if r:
                res.extend(r)
        return res

    res = fill_bits([], program)

    def bits_to_number(selected: list[int]):
        s = 0
        for i in reversed(selected):
            s = (s << 3) + (i % 8)
        return s

    numbers = [bits_to_number(r) for r in res]
    numbers = [n for n in numbers if list(run(n)) == program]
    return min(numbers)


print(sol())
