from days.day2.day2lib import get_ints, is_line_safe


def sol():
    c = 0
    for ints in get_ints():
        if is_line_safe(ints):
            c += 1
    return c


print(sol())
