from days.day3.day3lib import matches_2, eval_mul

def sol():
    total = 0
    enabled = True
    for match in matches_2():
        if match == "do()":
            enabled = True
        elif match == "don't()":
            enabled = False
        elif enabled:
            total += eval_mul(match)
    return total


print(sol())
