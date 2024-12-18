from lib.input import get_input
from lib.path import Pt

UP = Pt(0, -1)
RIGHT = Pt(1, 0)
DOWN = Pt(0, 1)
LEFT = Pt(-1, 0)


def sol():
    input = get_input()

    part_m, parm_i = input.split("\n\n")

    map_ = [list(x) for x in part_m.split("\n")]

    move_map = {"^": UP, ">": RIGHT, "v": DOWN, "<": LEFT}

    moves = [move_map[i] for i in parm_i if i in move_map]

    start = Pt(0, 0)
    for y, row in enumerate(map_):
        for x, cell in enumerate(row):
            if cell == "@":
                start = Pt(x, y)

    map_[start.y][start.x] = "."

    def print_map():
        for row in map_:
            print("".join(row))
        print()

    current_pt = start
    for move in moves:
        next_pt = current_pt + move
        if map_[next_pt.y][next_pt.x] == "O":
            boxes_inline = []
            box_pt = next_pt
            while True:
                boxes_inline.append(box_pt)
                next_box_pt = box_pt + move
                if map_[next_box_pt.y][next_box_pt.x] != "O":
                    break
                box_pt = next_box_pt

            pt_after_last_box = boxes_inline[-1] + move
            if map_[pt_after_last_box.y][pt_after_last_box.x] == "#":
                current_pt = current_pt
            else:
                map_[pt_after_last_box.y][pt_after_last_box.x] = "O"
                map_[next_pt.y][next_pt.x] = "."
                current_pt = next_pt

        elif map_[next_pt.y][next_pt.x] == ".":
            current_pt = next_pt
        elif map_[next_pt.y][next_pt.x] == "#":
            current_pt = current_pt
        # print(move, current_pt)
        # print_map()

    v = 0
    for y, row in enumerate(map_):
        for x, cell in enumerate(row):
            if cell == "O":
                v += 100 * y + x

    return v


print(sol())
