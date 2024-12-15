from lib.input import get_input
from lib.path import Pt

UP = Pt(0, -1)
RIGHT = Pt(1, 0)
DOWN = Pt(0, 1)
LEFT = Pt(-1, 0)


def sol():
    input = get_input()

    part_m, parm_i = input.split("\n\n")

    part_m_lines = [
        line.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")
        for line in part_m.split("\n")
    ]
    map_ = [list(x) for x in part_m_lines]

    move_map = {"^": UP, ">": RIGHT, "v": DOWN, "<": LEFT}

    moves = [move_map[i] for i in parm_i if i in move_map]

    start = Pt(0, 0)
    for y, row in enumerate(map_):
        for x, cell in enumerate(row):
            if cell == "@":
                start = Pt(x, y)

    map_[start.y][start.x] = "."

    def print_map(current_pt):
        map_copy = [list(x) for x in map_]
        map_copy[current_pt.y][current_pt.x] = "@"
        for row in map_copy:
            print("".join(row))
        print()

    print_map(start)

    def find_box_in_direction(box_left, box_right, direction):
        res = [(box_left, box_right)]
        if direction == RIGHT:
            right_to_right = box_right + direction
            if map_[right_to_right.y][right_to_right.x] == "[":
                res.extend(
                    find_box_in_direction(
                        right_to_right, right_to_right + direction, direction
                    )
                )
        if direction == LEFT:
            left_to_left = box_left + direction
            if map_[left_to_left.y][left_to_left.x] == "]":
                res.extend(
                    find_box_in_direction(
                        left_to_left + direction, left_to_left, direction
                    )
                )

        if direction == UP:
            up_to_left = box_left + direction
            up_to_left_char = map_[up_to_left.y][up_to_left.x]
            if up_to_left_char == "]":
                res.extend(
                    find_box_in_direction(up_to_left + LEFT, up_to_left, direction)
                )
            elif up_to_left_char == "[":
                res.extend(
                    find_box_in_direction(up_to_left, up_to_left + RIGHT, direction)
                )

            up_to_right = box_right + direction
            up_to_right_char = map_[up_to_right.y][up_to_right.x]
            if up_to_right_char == "[":
                res.extend(
                    find_box_in_direction(up_to_right, up_to_right + RIGHT, direction)
                )
            elif up_to_right_char == "]":
                res.extend(
                    find_box_in_direction(up_to_right + LEFT, up_to_right, direction)
                )

        if direction == DOWN:
            down_to_left = box_left + direction
            down_to_left_char = map_[down_to_left.y][down_to_left.x]
            if down_to_left_char == "]":
                res.extend(
                    find_box_in_direction(down_to_left + LEFT, down_to_left, direction)
                )
            elif down_to_left_char == "[":
                res.extend(
                    find_box_in_direction(down_to_left, down_to_left + RIGHT, direction)
                )

            down_to_right = box_right + direction
            down_to_right_char = map_[down_to_right.y][down_to_right.x]
            if down_to_right_char == "[":
                res.extend(
                    find_box_in_direction(
                        down_to_right, down_to_right + RIGHT, direction
                    )
                )
            elif down_to_right_char == "]":
                res.extend(
                    find_box_in_direction(
                        down_to_right + LEFT, down_to_right, direction
                    )
                )
        return res

    def move_boxes(boxes, direction) -> bool:
        all_pts = set()
        for left, right in boxes:
            all_pts.add(left)
            all_pts.add(right)

        # check if can move
        for pt in all_pts:
            next_ = pt + direction
            if map_[next_.y][next_.x] == "#":
                return False

        # set all boxes to empty
        for left, right in boxes:
            map_[left.y][left.x] = "."
            map_[right.y][right.x] = "."

        for left, right in boxes:
            left_next = left + direction
            right_next = right + direction
            map_[left_next.y][left_next.x] = "["
            map_[right_next.y][right_next.x] = "]"

        return True

    current_pt = start
    for move in moves:
        next_pt = current_pt + move
        if map_[next_pt.y][next_pt.x] in "[]":
            left = None
            right = None
            if map_[next_pt.y][next_pt.x] == "[":
                left = next_pt
                right = next_pt + RIGHT
            elif map_[next_pt.y][next_pt.x] == "]":
                left = next_pt + LEFT
                right = next_pt
            boxes_in_line = find_box_in_direction(left, right, move)
            if move_boxes(boxes_in_line, move):
                current_pt = next_pt
        elif map_[next_pt.y][next_pt.x] == ".":
            current_pt = next_pt
        elif map_[next_pt.y][next_pt.x] == "#":
            current_pt = current_pt

    # print_map(current_pt)
    v = 0
    for y, row in enumerate(map_):
        for x, cell in enumerate(row):
            if cell == "[":
                v += 100 * y + x

    return v


print(sol())
