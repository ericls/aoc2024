from lib.input import get_input
from lib.measure import print_runtime


def evolve(n):
    n = ((n << 6) ^ n) % 16777216
    n = ((n >> 5) ^ n) % 16777216
    n = ((n << 11) ^ n) % 16777216
    return n


def evolv_x(n, x):
    for _ in range(x):
        n = evolve(n)
    return n


@print_runtime
def sol():
    ints = map(int, get_input().splitlines())
    return sum(evolv_x(i, 2000) for i in ints)


print(sol())
