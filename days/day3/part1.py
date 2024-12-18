from days.day3.day3lib import eval_mul, matches_1
from lib.measure import print_runtime


@print_runtime
def sol():
    return sum(eval_mul(match) for match in matches_1())


print(sol())
