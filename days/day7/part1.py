from days.day7.day7lib import can_be_true, get_eqs


def sol():
    return sum(eq[0] for eq in get_eqs() if can_be_true(eq[0], eq[1], use_combo=False))


print(sol())
