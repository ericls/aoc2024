from bisect import bisect_left, bisect_right, insort
from heapq import merge
from typing import NamedTuple


def bisect_index(sorted_list, item, key):
    left_index = bisect_left(sorted_list, key(item), key=key)
    right_index = bisect_right(sorted_list, key(item), key=key)

    for index in range(left_index, right_index):
        if sorted_list[index] == item:
            return index

    raise ValueError("Item not found in list")


class Chunk(NamedTuple):
    loc: int
    file_id: int
    size: int


class Disk:
    file_chunks: list[Chunk]  # sorted by loc
    free_spaces: list[Chunk]  # sorted by loc
    file_chunks_by_id: dict[int, list[Chunk]]
    free_spaces_by_size: dict[int, list[Chunk]]

    def __init__(self, file_chunks: list[Chunk], free_spaces: list[Chunk]) -> None:
        self.file_chunks = file_chunks
        self.free_spaces = free_spaces
        self.file_chunks_by_id = {
            file_chunk.file_id: [file_chunk] for file_chunk in file_chunks
        }
        self.free_spaces_by_size = {}
        for chunk in free_spaces:
            insort(
                self.free_spaces_by_size.setdefault(chunk.size, []),
                chunk,
                key=lambda c: c.loc,
            )

    @classmethod
    def from_ints(cls, ints: list[int]):
        file_count = 0
        files = []
        free_spaces = []
        loc = 0
        for index, digit in enumerate(ints):
            if index % 2 == 0:
                file = Chunk(loc, file_count, digit)
                files.append(file)
                file_count += 1
            else:
                space = Chunk(loc, -1, digit)
                if digit > 0:
                    free_spaces.append(space)
            loc += digit
        return cls(files, free_spaces)

    @property
    def str_content(self):  # for debugging
        s = ""
        for chunk in merge(self.file_chunks, self.free_spaces):
            s += f"{chunk.file_id if chunk.file_id != -1 else '.'}" * chunk.size
        return s

    @property
    def first_space_loc(self):
        return self.free_spaces[0].loc

    @property
    def last_file_loc(self):
        return self.file_chunks[-1].loc

    @property
    def checksum(self):
        checksum = 0
        for file_chunk in self.file_chunks:
            for i in range(file_chunk.size):
                checksum += file_chunk.file_id * (file_chunk.loc + i)
        return checksum

    def move(self, file_index: int, space_index: int):
        file_chunk = self.file_chunks[file_index]
        space_chunk = self.free_spaces[space_index]

        file_size = file_chunk.size
        to_size = space_chunk.size
        file_id = file_chunk.file_id

        if file_size > to_size:
            new_to = [Chunk(space_chunk.loc, file_id, to_size)]
            new_from = [
                Chunk(file_chunk.loc, file_id, file_size - to_size),
                Chunk(file_chunk.loc + file_size - to_size, -1, to_size),
            ]
            new_chunks = new_to + new_from
        elif file_size < to_size:
            new_to = [
                Chunk(space_chunk.loc, file_id, file_size),
                Chunk(space_chunk.loc + file_size, -1, to_size - file_size),
            ]
            new_from = [Chunk(file_chunk.loc, -1, file_size)]
            new_chunks = new_to + new_from
        else:
            new_to = [Chunk(space_chunk.loc, file_id, to_size)]
            new_from = [Chunk(file_chunk.loc, -1, file_size)]
            new_chunks = new_to + new_from

        self.remove_file_by_index(file_index)
        self.remove_space_by_index(space_index)

        for chunk in new_chunks:
            if chunk.file_id == -1:
                self.add_space_chunk(chunk)
            else:
                self.add_file_chunk(chunk)

    def remove_file_by_index(self, file_index: int):
        file_chunk = self.file_chunks[file_index]
        file_id = file_chunk.file_id
        self.file_chunks.pop(file_index)
        self.file_chunks_by_id[file_id].remove(file_chunk)  # should be small list

    def add_file_chunk(self, chunk: Chunk):
        insort(self.file_chunks, chunk, key=lambda chunk: chunk.loc)
        self.file_chunks_by_id.setdefault(chunk.file_id, []).append(chunk)
        self.file_chunks_by_id[chunk.file_id].sort(key=lambda chunk: chunk.loc)

    def remove_space_by_index(self, space_index: int):
        space_chunk = self.free_spaces[space_index]
        self.free_spaces.pop(space_index)
        self.free_spaces_by_size[space_chunk.size].remove(space_chunk)

    def add_space_chunk(self, chunk: Chunk):
        insort(self.free_spaces, chunk, key=lambda c: c.loc)
        insort(
            self.free_spaces_by_size.setdefault(chunk.size, []),
            chunk,
            key=lambda c: c.loc,
        )

    def get_file_chunk_index(self, chunk: Chunk):
        return bisect_left(self.file_chunks, chunk.loc, key=lambda chunk: chunk.loc)

    def available_space_index(self, file_chunk: Chunk):
        selected_chunks = []
        for size in range(file_chunk.size, 10):
            if size in self.free_spaces_by_size:
                space_chunks = self.free_spaces_by_size[size]
                if not space_chunks:
                    continue
                space_chunk = space_chunks[0]
                if space_chunk.loc > file_chunk.loc:
                    continue
                selected_chunks.append(space_chunk)
        if not selected_chunks:
            return None
        selected = min(selected_chunks, key=lambda chunk: chunk.loc)
        return bisect_index(self.free_spaces, selected, key=lambda chunk: chunk.loc)
