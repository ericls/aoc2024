from days.day1.day1lib import get_day1_input
from lib.measure import print_runtime


@print_runtime
def sol():
    la, lb = get_day1_input()
    la.sort()
    lb.sort()

    return sum(abs(a - b) for a, b in zip(la, lb))


print(sol())
