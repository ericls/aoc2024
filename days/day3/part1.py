from days.day3.day3lib import matches_1, eval_mul

def sol():
    return sum(
        eval_mul(match)
        for match in matches_1()
    )


print(sol())
