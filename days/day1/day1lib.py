from lib.input import get_input_lines


def get_day1_input():
    input_lines = get_input_lines()

    la = []
    lb = []
    for line in input_lines:
        a, b = [int(x) for x in line.split()]
        la.append(a)
        lb.append(b)

    return la, lb
