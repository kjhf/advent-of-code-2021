from math import floor
from statistics import median, mean
from typing import List

from src.common import get_input


def day_7():
    # Puzzle input is a list of the horizontal position of each crab.
    # Fuel usage is the difference between the current state and the alignment target.
    # Determine the horizontal position that the crabs can align to using the least fuel possible (and submit that).
    input_lines = get_input(day=7)
    fuels = [int(fuel) for fuel in input_lines[0].split(',') if fuel]
    med = floor(median(fuels))
    one_below = med - 1
    one_above = med + 1
    print("Part 1 Median:")
    calculate_alignment_part_1(fuels, med)
    print("-----")
    calculate_alignment_part_1(fuels, one_below)
    calculate_alignment_part_1(fuels, one_above)

    mean_val = floor(mean(fuels))
    one_below = mean_val - 1
    one_above = mean_val + 1
    print("-----")
    print("Part 2 Floored Mean:")
    calculate_alignment_part_2(fuels, mean_val)
    print("-----")
    calculate_alignment_part_2(fuels, one_below)
    calculate_alignment_part_2(fuels, one_above)


def calculate_alignment_part_1(fuels: List[int], align: int):
    """For part 1, alignment is linear difference"""
    result = sum([abs(fuel - align) for fuel in fuels])
    print(f"Aligned to {align} gives {result}")


def calculate_alignment_part_2(fuels: List[int], align: int):
    """For part 2, alignment is n/2 (n+1) difference"""
    result = sum([fuel_cost_part_2(abs(fuel - align)) for fuel in fuels])
    print(f"Aligned to {align} gives {result}")


def fuel_cost_part_2(diff: int):
    """
    AP sequence: n/2 (n+1)
    i.e. diff | 0  1  2  3   4   5 ...
    fuel cost | 0  1  3  6  10  15 ...
    """
    return (0.5 * diff) * (diff + 1)


if __name__ == '__main__':
    day_7()
