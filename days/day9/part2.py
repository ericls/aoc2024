from days.day9.day9lib import Disk
from lib.input import get_input


def sol():
    input = get_input()
    ints = [int(c) for c in input]
    disk = Disk.from_ints(ints)
    max_file_id = max(disk.file_chunks_by_id.keys())

    def find_space(file_id):
        file_chunks = disk.file_chunks_by_id[file_id]
        file_chunk = file_chunks[0]
        return disk.available_space_index(file_chunk)

    for file_id in range(max_file_id, -1, -1):
        space_index = find_space(file_id)
        if space_index is not None:
            file_chunks = disk.file_chunks_by_id[file_id]
            file_chunk = file_chunks[0]
            disk.move(disk.get_file_chunk_index(file_chunk), space_index)
    return disk.checksum


print(sol())
