from days.day13.day13lib import parse_input, solve_eq
from lib.input import get_input


def sol():
    input = get_input()
    consts = parse_input(input)
    total = 0
    for const in consts:
        a, b = solve_eq(*const)
        if int(a) == a and int(b) == b:
            total += int(3 * a + b)
    return total


print(sol())
