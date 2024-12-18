from days.day9.day9lib import Disk
from lib.input import get_input
from lib.measure import print_runtime


@print_runtime
def sol():
    input = get_input()
    ints = [int(c) for c in input]
    disk = Disk.from_ints(ints)
    while disk.first_space_loc < disk.last_file_loc:
        last_file_index = len(disk.file_chunks) - 1
        first_space_index = 0
        disk.move(last_file_index, first_space_index)

    return disk.checksum


print(sol())
