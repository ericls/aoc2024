from days.day2.day2lib import get_ints, is_line_safe, produce_ints
from lib.measure import print_runtime


@print_runtime
def sol():
    c = 0
    for ints in get_ints():
        for child_ints in produce_ints(ints):
            if is_line_safe(child_ints):
                c += 1
                break
    return c


print(sol())
