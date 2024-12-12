from functools import cache


@cache
def evolve(n: int):
    if n == 0:
        return [1]
    else:
        digits = len(str(n))
        if digits % 2 == 0:
            return [
                int(str(n)[: digits // 2]),
                int(str(n)[digits // 2 :]),
            ]
        else:
            return [n * 2024]


@cache
def len_evolve_x_times(n: int, x: int):
    if x == 0:
        return 1
    res = 0
    for i in evolve(n):
        res += len_evolve_x_times(i, x - 1)
    return res
