from typing import List, Optional

from src.common import get_input


def day_9():
    # The input is a heightmap - find the lowest points in the sequence (which is lower than its adjacent neighbours)
    # The score "risk level" is the value + 1, summed
    input_lines = get_input(day=9)

    # As with Day 4, pandas would be a good solution to this.
    heightmap: List[List[int]] = []
    
    # I know this can be done as a double list comp but let's face it, this is more readable.
    for line in input_lines:
        heightmap.append([int(val) for val in line.strip()])
    
    assert heightmap, "No input?"
    number_of_rows = len(input_lines)

    low_points = []
    for row_i, line in enumerate(heightmap):
        for val_i, val in enumerate(line):
            neighbours = get_neighbours(
                previous_row=heightmap[row_i - 1] if row_i else None,
                current_row=heightmap[row_i],
                next_row=heightmap[row_i + 1] if (row_i + 1) < number_of_rows else None,
                cell_i=val_i
            )

            if is_low_point(val, neighbours):
                low_points.append(val)

    print(f"{low_points=}")
    risk = calculate_score(low_points)
    print(f"{risk=}")


def get_neighbours(previous_row: Optional[List[int]], current_row: List[int], next_row: Optional[List[int]], cell_i: int) -> List[int]:
    result = []
    if previous_row is not None:
        result.append(previous_row[cell_i])
    if cell_i:
        result.append(current_row[cell_i - 1])
    if (cell_i + 1) < len(current_row):
        result.append(current_row[cell_i + 1])
    if next_row is not None:
        result.append(next_row[cell_i])
    return result


def is_low_point(this_point: int, neighbours: List[int]) -> bool:
    return this_point < min(neighbours)


def calculate_score(lows: List[int]) -> int:
    return sum(val + 1 for val in lows)


if __name__ == '__main__':
    day_9()
