from functools import cache

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
    def shortest_paths_segments_for_sequence(self, start: Pt, sequence: str):
        curr = start
        segments: list[list[str]] = []
        while sequence:
            next_target_pt = self.str_to_pos[sequence[0]]
            segments.append(self.shortest_paths(curr, next_target_pt))
            curr = next_target_pt
            sequence = sequence[1:]
        total_length = sum(len(s[0]) for s in segments)
        return segments, total_length

    def select(self, start: Pt, sequences: list[str]):
        map_ = {
            sequence: self.shortest_paths_segments_for_sequence(start, sequence)
            for sequence in sequences
        }
        return min(map_.values(), key=lambda x: x[1]), self.str_to_pos[sequences[0][-1]]

    def shortest_paths_segments_for_segments(
        self, start: Pt, segments: list[list[str]]
    ):
        cur = start
        res = []
        for segment in segments:
            (selected, length), nest_pos = self.select(cur, segment)
            res.extend(selected)
            cur = nest_pos
        return res

    @cache
    def length_after_x(self, sequence: str, x: int):
        if x == 0:
            return len(sequence)
        length = 0
        segments, _ = self.shortest_paths_segments_for_sequence(self.start, sequence)
        for segment in segments:
            length += min(self.length_after_x(choice, x - 1) for choice in segment)
        return length

    def segments_legnth_after_x(self, segments: list[list[str]], x: int):
        if x == 0:
            return sum(len(s[0]) for s in segments)
        length = 0
        for segment in segments:
            length += min(self.length_after_x(choice, x - 1) for choice in segment)
        return length


D_PAD = Pad(D_PAD_LAYOUT)
NUM_PAD = Pad(NUM_PAD_LAYOUT)


@print_runtime
def sol():
    input = get_input()

    def key_presses(code: str):
        d_pad_segments = NUM_PAD.shortest_paths_segments_for_segments(
            NUM_PAD.start, [[code]]
        )
        length = D_PAD.segments_legnth_after_x(d_pad_segments, 26)
        return length

    return sum(int(line[:-1]) * key_presses(line) for line in input.splitlines())


print(sol())
