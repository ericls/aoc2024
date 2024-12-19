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
    def validate(rem):
        if not rem:
            return True
        new_rems = []
        for seg in segments:
            if rem.startswith(seg):
                new_rems.append(rem[len(seg) :])
        return any(validate(new_rem) for new_rem in new_rems)

    return sum(1 for _ in (w for w in words if validate(w)))


print(sol())
