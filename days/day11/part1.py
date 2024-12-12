from days.day11.day11lib import len_evolve_x_times
from lib.input import get_input


def sol():
    input = get_input()
    stones = [int(i) for i in input.split()]
    return sum(len_evolve_x_times(i, 25) for i in stones)


print(sol())
