from collections import Counter

from days.day1.day1lib import get_day1_input
from lib.measure import print_runtime


@print_runtime
def sol():
    la, lb = get_day1_input()
    counts = Counter(la)

    return sum(b * counts[b] for b in lb)


print(sol())
