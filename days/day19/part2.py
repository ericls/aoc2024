from functools import cache

from lib.input import get_input
from lib.measure import print_runtime


@print_runtime
def sol():
    input = get_input()
    segments_line, words_lines = input.split("\n\n")
    segments = segments_line.split(", ")
    words = words_lines.split("\n")

    @cache
    def ways(rem):
        if not rem:
            return 1
        new_rems = []
        for seg in segments:
            if rem.startswith(seg):
                new_rems.append(rem[len(seg) :])
        return sum(ways(new_rem) for new_rem in new_rems)

    sum_ways = 0
    for word in words:
        sum_ways += ways(word)

    return sum_ways


print(sol())
