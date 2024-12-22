from collections import defaultdict, deque
from itertools import chain, pairwise

from lib.input import get_input
from lib.measure import print_runtime


def evolve(n):
    n = ((n << 6) ^ n) % 16777216
    n = ((n >> 5) ^ n) % 16777216
    n = ((n << 11) ^ n) % 16777216
    yield n


def evolv_x(n, x):
    yield n
    for _ in range(x):
        n = next(evolve(n))
        yield n


def get_prices(n):
    yield from (i % 10 for i in evolv_x(n, 2000))


def diff(o):
    return o[1] - o[0]


def gen_seq_price(n):
    prices = get_prices(n)
    first_4 = [next(prices) for _ in range(4)]
    prev_diffs = deque([diff(pair) for pair in pairwise(first_4)], maxlen=4)
    last_p = first_4[-1]
    seen = set()
    for p in prices:
        new_diff = p - last_p
        prev_diffs.append(new_diff)
        prefix = tuple(prev_diffs)
        last_p = p
        if prefix in seen:
            continue
        yield prefix, p
        seen.add(prefix)


@print_runtime
def sol():
    ints = map(int, get_input().splitlines())

    total_for_key = defaultdict(int)
    for k, v in chain.from_iterable(gen_seq_price(i) for i in ints):
        total_for_key[k] += v

    return max(total_for_key.values())


print(sol())
