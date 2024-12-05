from collections import defaultdict

from lib.input import get_input


def get_order_rules_and_ints_list():
    section1, section2 = get_input().split("\n\n")
    order_rule_lines = section1.splitlines()
    updates_lines = section2.splitlines()
    order_rules = defaultdict(list)

    for line in order_rule_lines:
        a, b = map(int, line.split("|"))
        order_rules[a].append(b)

    ints_list = []
    for line in updates_lines:
        ints_list.append(list(map(int, line.split(","))))

    return order_rules, ints_list


def is_in_order(order_rules, ints):
    for i in range(len(ints) - 1):
        a = ints[i]
        for j in range(i + 1, len(ints)):
            b = ints[j]
            if a in order_rules[b]:
                return False
    return True


def order_ints(order_rules, ints):
    if len(ints) == 0:
        return []
    if len(ints) == 1:
        return ints
    a, *rest = ints

    rest_after_a = [i for i in rest if i in order_rules[a]]
    rest_before_a = [i for i in rest if i not in rest_after_a]

    return (
        order_ints(order_rules, rest_before_a)
        + [a]
        + order_ints(order_rules, rest_after_a)
    )
