from typing import List

from src.common import get_input

from dataclasses import dataclass


@dataclass
class Vector:
    x_start: int
    x_end: int
    y_start: int
    y_end: int

    @staticmethod
    def from_str(parse: str):
        parts = parse.partition("->")
        start = parts[0].strip().partition(",")
        end = parts[2].strip().partition(",")

        x_start = int(start[0].strip())
        x_end = int(end[0].strip())
        y_start = int(start[2].strip())
        y_end = int(end[2].strip())

        return Vector(
            x_start=x_start,
            x_end=x_end,
            y_start=y_start,
            y_end=y_end
        )

    @property
    def x_diff(self):
        return self.x_end - self.x_start

    @property
    def x_changing(self):
        return self.x_start != self.x_end

    @property
    def y_diff(self):
        return self.y_end - self.y_start

    @property
    def y_changing(self):
        return self.y_start != self.y_end


def day_5():
    input_lines = get_input(day=5)

    # x1,y1 -> x2,y2
    # 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
    # For part 1, consider horizontal and vertical lines (x1 = x2 or y1 = y2)
    # For part 2,
    # An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
    # An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.
    all_vectors = [Vector.from_str(line) for line in input_lines]
    part_1_vectors = [v for v in all_vectors if (v.x_start == v.x_end) or (v.y_start == v.y_end)]
    print(f"{len(all_vectors)} vectors loaded, of which we're looking at {len(part_1_vectors)} for part 1. "
          f"First loaded vector is {all_vectors[0]}, and the last is {all_vectors[-1]}.")

    print("Part 1: ")
    do_the_thing(part_1_vectors)
    print("\nPart 2: ")
    do_the_thing(all_vectors)


def do_the_thing(vectors: List[Vector]):
    # Init the board
    row_size = 1000
    board = [0] * (row_size ** 2)

    # Insert all the vectors
    for v in vectors:
        for i in range(0, max(abs(v.x_diff), abs(v.y_diff)) + 1):
            x_i = i if v.x_diff > 0 else -i if v.x_diff < 0 else 0
            y_i = i if v.y_diff > 0 else -i if v.y_diff < 0 else 0
            board[get_index(v.x_start + x_i, v.y_start + y_i, row_size)] += 1

    # Score is how many points do at least two lines overlap?
    score = len([cell for cell in board if cell > 1])
    print(f"{score=}")

    # Print a board to file because why not
    dump_board(board, row_size)


def dump_board(board: List[int], row_size: int):
    file_content = []
    for i in range(0, row_size):
        file_content.append(' '.join([f"{cell:01}" for cell in board[i * row_size:(i + 1) * row_size]]) + '\n')
    with open(file="board.txt", mode='w', encoding='utf-8') as the_file:
        the_file.writelines(file_content)


def get_index(x: int, y: int, row_size: int):
    return x + (y * row_size)


if __name__ == '__main__':
    day_5()
