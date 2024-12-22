from functools import cache
from itertools import product

from lib.input import get_input
from lib.measure import print_runtime
from lib.path import Pt

UP = Pt(0, -1)
DOWN = Pt(0, 1)
LEFT = Pt(-1, 0)
RIGHT = Pt(1, 0)

NUM_PAD_LAYOUT = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], [None, "0", "A"]]

D_PAD_LAYOUT = [
    [None, "^", "A"],
    ["<", "v", ">"],
]

D_MAP = {"^": UP, "v": DOWN, "<": LEFT, ">": RIGHT}

D_MAP_REV = {UP: "^", DOWN: "v", LEFT: "<", RIGHT: ">"}


def path_to_str(path):
    return "".join([D_MAP_REV[p] for p in path])


class Pad:
    def __init__(self, pad):
        self.pad = pad
        self.start = Pt(0, 0)
        self.str = "".join("".join([str(i) for i in row]) for row in self.pad)

        for y, row in enumerate(pad):
            for x, val in enumerate(row):
                if val == "A":
                    self.start = Pt(x, y)

        self.str_to_pos = {
            val: Pt(x, y)
            for y, row in enumerate(pad)
            for x, val in enumerate(row)
            if val is not None
        }

    def inbound(self, pt):
        x, y = pt
        return (
            0 <= y < len(self.pad)
            and 0 <= x < len(self.pad[y])
            and self.pad[y][x] is not None
        )

    def __hash__(self) -> int:
        return hash(self.str)

    @cache
    def shortest_paths(self, start: Pt, target: Pt):
        if start == target:
            return ["A"]
        distance = abs(target.x - start.x) + abs(target.y - start.y)
        res = []
        for direction in [UP, DOWN, LEFT, RIGHT]:
            nb = start + direction
            if not self.inbound(nb):
                continue
            distance_nb = abs(target.x - nb.x) + abs(target.y - nb.y)
            if distance_nb >= distance:
                continue
            if nb == target:
                res.append(D_MAP_REV[direction] + "A")
                continue
            rest = self.shortest_paths(nb, target)
            for r in rest:
                res.append(D_MAP_REV[direction] + r)
        min_length = min([len(r) for r in res])
        res = [r for r in res if len(r) == min_length]
        return res

    @cache
    def shortest_paths_segments_for_sequence(self, sequence: str):
        curr = self.start
        path = []
        while sequence:
            next_target_pt = self.str_to_pos[sequence[0]]
            path.append(self.shortest_paths(curr, next_target_pt))
            curr = next_target_pt
            sequence = sequence[1:]
        return path

    @cache
    def shortest_length_for_sequence(self, sequence: str):
        curr = self.start
        length = 0
        while sequence:
            next_target_pt = self.str_to_pos[sequence[0]]
            length += len(self.shortest_paths(curr, next_target_pt)[0])
            curr = next_target_pt
            sequence = sequence[1:]
        return length

    @cache
    def shortest_paths_for_sequence(self, sequence: str):
        segments = self.shortest_paths_segments_for_sequence(sequence)
        results = []
        for combo in product(*segments):
            results.append("".join(combo))
        return results

    def shortest_paths_for_sequences(self, sequences):
        res = []
        for sequence in sequences:
            res.extend(self.shortest_paths_for_sequence(sequence))
        min_length = min([len(r) for r in res])
        res = [r for r in res if len(r) == min_length]
        return res


D_PAD = Pad(D_PAD_LAYOUT)
NUM_PAD = Pad(NUM_PAD_LAYOUT)


def get_key_press(pads, target):
    cur = [target]
    for pad in pads:
        cur = pad.shortest_paths_for_sequences(cur)
    return cur


def get_length_of_key_press(pads, target) -> int:
    prev_pad, last_pad = pads[:-1], pads[-1]
    return min(
        last_pad.shortest_length_for_sequence(k)
        for k in get_key_press(prev_pad, target)
    )


@print_runtime
def sol():
    input = get_input()
    pads = [NUM_PAD, D_PAD, D_PAD]
    return sum(
        int(line[:-1]) * get_length_of_key_press(pads, line)
        for line in input.splitlines()
    )


print(sol())
