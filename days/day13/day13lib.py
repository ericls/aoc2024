import re

digits = re.compile(r"\d+")


def parse_input(input):
    blocks = input.strip().split("\n\n")

    result = []
    for block in blocks:
        lines = block.split("\n")

        block_tuple = tuple(tuple(map(int, digits.findall(line))) for line in lines)
        result.append(block_tuple)

    return result


def solve_eq(a, b, c):
    x1 = a[0]
    y1 = a[1]
    x2 = b[0]
    y2 = b[1]

    x3 = c[0]
    y3 = c[1]

    # a * x1 + b * x2 = x3
    # a * y1 + b * y2 = y3

    a = (x3 * y2 - x2 * y3) / (x1 * y2 - x2 * y1)
    b = (x1 * y3 - x3 * y1) / (x1 * y2 - x2 * y1)

    return a, b
