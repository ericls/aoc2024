from days.day5.day5lib import get_order_rules_and_ints_list, is_in_order, order_ints
from lib.measure import print_runtime


@print_runtime
def sol():
    order_rules, ints_list = get_order_rules_and_ints_list()
    incorrect_ints = [ints for ints in ints_list if not is_in_order(order_rules, ints)]
    return sum(order_ints(order_rules, ints)[len(ints) // 2] for ints in incorrect_ints)


print(sol())
