import re
from lib.input import get_input

mul_regex = r"mul\(\d+,\d+\)"
do_regex = r"do\(\)"
dont_regex = r"don\'t\(\)"

all_regex = f"({mul_regex}|{do_regex}|{dont_regex})"


def eval_mul(expression):
    a, b = map(
        int, expression.replace("mul", "").replace("(", "").replace(")", "").split(",")
    )
    return a * b


def matches_1():
    line = get_input()
    matches = re.findall(mul_regex, line)
    for match in matches:
        yield match


def matches_2():
    line = get_input()
    matches = re.findall(all_regex, line)
    for match in matches:
        yield match
