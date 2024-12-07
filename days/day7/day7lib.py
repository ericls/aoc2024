from lib.input import get_input


def concat_ints(a, b):
    for scale in [10, 100, 1000]:
        if b < scale:
            return a * scale + b


def can_be_true(target, ints, use_combo=False):
    def inner(head, i):
        if target < head:
            return False
        if i == len(ints):
            return target == head
        a = head
        b = ints[i]

        return (
            inner(a * b, i + 1)
            or inner(a + b, i + 1)
            or (use_combo and inner(concat_ints(a, b), i + 1))
        )

    return inner(ints[0], 1)


def get_eqs():
    lines = get_input().splitlines()

    eqs = []
    for line in lines:
        target, ints = line.split(": ")
        target = int(target)
        ints = list(map(int, ints.split()))
        eqs.append((target, ints))

    return eqs
