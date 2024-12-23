from collections import defaultdict

from lib.input import get_input
from lib.measure import print_runtime


@print_runtime
def sol(input):
    lines = input.splitlines()
    graph = defaultdict(set)
    for line in lines:
        a, b = line.split("-")
        graph[a].add(b)
        graph[b].add(a)

    sets = set()
    for k, vs in graph.items():
        for v in vs:
            if v == k:
                continue
            for vv in graph[v]:
                if vv == k:
                    continue
                if k in graph[vv]:
                    sets.add(tuple(sorted([k, v, vv])))

    count = 0
    for s in sets:
        if any(i.startswith("t") for i in s):
            count += 1
    return count


print(sol(get_input()))
