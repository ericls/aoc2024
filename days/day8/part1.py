from days.day8.day8lib import count_locations, gen_locations_1, get_map
from lib.measure import print_runtime


@print_runtime
def sol():
    (width, height), ants = get_map()
    return count_locations(gen_locations_1, ants, width, height)


print(sol())
