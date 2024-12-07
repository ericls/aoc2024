from lib.input import get_input


def can_be_true(target, ints, use_combo=False):
    if len(ints) == 1:
        return target == ints[0]

    a, b, *rest = ints

    return (
        can_be_true(target, [a * b] + rest, use_combo=use_combo)
        or can_be_true(target, [a + b] + rest, use_combo=use_combo)
        or (
            use_combo
            and can_be_true(target, [int(str(a) + str(b))] + rest, use_combo=use_combo)
        )
    )


def get_eqs():
    lines = get_input().splitlines()

    eqs = []
    for line in lines:
        target, ints = line.split(": ")
        target = int(target)
        ints = list(map(int, ints.split()))
        eqs.append((target, ints))

    return eqs
