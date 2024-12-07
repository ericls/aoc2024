from lib.input import get_input


def can_be_true(target, ints, use_combo=False):
    if not ints:
        return False
    if len(ints) == 1:
        return target == ints[0]

    a, b, *rest = ints

    res_multi = can_be_true(target, [a * b] + rest, use_combo=use_combo)
    res_add = can_be_true(target, [a + b] + rest, use_combo=use_combo)
    if use_combo:
        res_combo = can_be_true(
            target, [int(str(a) + str(b))] + rest, use_combo=use_combo
        )
    else:
        res_combo = False

    return res_add or res_multi or res_combo


def get_eqs():
    lines = get_input().splitlines()

    eqs = []
    for line in lines:
        target, ints = line.split(": ")
        target = int(target)
        ints = list(map(int, ints.split()))
        eqs.append((target, ints))

    return eqs
