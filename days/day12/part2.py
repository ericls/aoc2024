from days.day12.day12lib import Area, Grid
from lib.input import get_input
from lib.measure import print_runtime


@print_runtime
def sol():
    input = get_input()
    lines = input.splitlines()
    grid = Grid([[c for c in line] for line in lines])
    areas = Area.build_areas(grid)

    return sum(a.bulk_cost for a in areas)


print(sol())
