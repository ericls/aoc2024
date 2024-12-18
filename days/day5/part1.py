from days.day5.day5lib import get_order_rules_and_ints_list, is_in_order
from lib.measure import print_runtime


@print_runtime
def sol():
    order_rules, ints_list = get_order_rules_and_ints_list()
    return sum(
        ints[len(ints) // 2] for ints in ints_list if is_in_order(order_rules, ints)
    )


print(sol())
