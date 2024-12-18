from lib.input import get_input
from lib.measure import print_runtime
from lib.path import Pt


@print_runtime
def sol():
    input = get_input()
    width = 101
    height = 103
    ps = []
    vs = []
    for line in input.splitlines():
        line = line.removeprefix("p=")
        a, b = line.split(" v=")
        p = a.split(",")
        v = b.split(",")
        ps.append(Pt(int(p[0]), int(p[1])))
        vs.append(Pt(int(v[0]), int(v[1])))

    def wrap(pt):
        return Pt(pt.x % width, pt.y % height)

    def print_ps(ps):
        field_line = ["." for _ in range(width)]
        field = [[i for i in field_line] for _ in range(height)]
        for p in ps:
            field[p.y][p.x] = "#"
        for line in field:
            line_str = "".join(line)
            # if "#####################" in line_str:
            #     print("FUCK@@@@@@@@@")
            print(line_str)
        print("=====================================")

    def is_ps_symetric(ps):  # this doesn't work, the graph is not symetric
        ps_set = set(ps)
        for p in ps_set:
            if Pt(width - p.x - 1, p.y) not in ps_set:
                return False
        return True

    def all_unique(ps):
        return len(set(ps)) == len(ps)

    def detect_cluster(
        ps,
    ):  # this works, but the above is so much easier, check cluster size > 200
        def flood_fill(start, ps_set, visited):
            stack = [start]
            cluster = []
            while stack:
                p = stack.pop()
                if p in visited:
                    continue
                visited.add(p)
                cluster.append(p)
                for neighbor in p.nb8:
                    if neighbor in ps_set and neighbor not in visited:
                        stack.append(neighbor)
            return cluster

        ps_set = set(ps)
        visited = set()
        for p in ps_set:
            if p not in visited:
                yield len(flood_fill(p, ps_set, visited))

    i = 0
    while True:
        after_move = []
        for p, v in zip(ps, vs):
            after_move.append(wrap(p + (v * i)))
        # if is_ps_symetric(after_move):
        #     return i
        if all_unique(after_move):
            return i
        # if any([cluster > 200 for cluster in detect_cluster(after_move)]):
        #     return i
        i += 1
        # print(i)


print(sol())
