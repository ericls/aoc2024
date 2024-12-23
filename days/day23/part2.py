from lib.input import get_input
from lib.measure import print_runtime


@print_runtime
def sol(input):
    lines = input.splitlines()
    edges = set()
    names = set()
    for line in lines:
        a, b = line.split("-")
        edges.add((a, b))
        edges.add((b, a))
        names.add(a)
        names.add(b)

    sets = []
    for name in names:
        for s in sets:
            if all((i, name) in edges for i in s):
                s.add(name)
        sets.append(set([name]))

    largest = max(sets, key=lambda s: len(s))

    return ",".join(sorted(largest))


print(sol(get_input()))
