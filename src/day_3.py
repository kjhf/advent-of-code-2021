from collections import Counter
from typing import Literal, List

from src.common import get_input


def day_3_part_1():
    """
    The power consumption can be found by gamma * epsilon.
    Considering only the first bit of each number, the first bit of the gamma rate is most common 0 or 1
    Considering only the second bit of each number, the second bit of the gamma rate is most common 0 or 1 etc
    Then convert the bits to dec.
    epsilon rate is calculated in a similar way but the least common bit is used [Slate's note: bit-wise compliment]
    """
    input_lines = get_input(day=3)
    line_length = len(input_lines[0])  # this is the number of loops/number of bits

    gamma = ""
    epsilon = ""
    for column in range(0, line_length):
        column_sequence = [line[column] for line in input_lines]
        most_common_tups = Counter(column_sequence).most_common()
        gamma += most_common_tups[0][0]  # gamma uses most common
        epsilon += most_common_tups[-1][0]  # epsilon uses least common

    # Convert bits sequence to dec
    gamma = int(gamma, 2)
    epsilon = int(epsilon, 2)

    # You can also work out epsilon from gamma by doing compliment (so epsilon above is not needed)
    epsilon_check = ~gamma + 2 ** line_length
    print(f"{gamma=}, {epsilon=}, {gamma * epsilon=}, {epsilon_check=}")


def day_3_part_2():
    """
    The life support rating = oxygen generator * CO2 scrubber.
    Start with the full list of binary numbers and consider just the first bit.

    To find oxygen generator, determine the most common value (0 or 1) in the current bit position,
    and keep only numbers with that bit in that position (or 1).
    To find CO2 scrubber, determine the least common value (0 or 1) in the current bit position,
    and keep only numbers with that bit in that position (or 0).
    If you only have one number left, stop; this is the rating value for which you are searching.
    Otherwise, repeat the process, considering the next bit to the right.

    Start with all lines of data and consider only the first bit of each number.
    If there are more 1 bits (7) than 0 bits (5), keep only the 7 numbers with a 1 in the first position: 11110, 10110, 10111, 10101, 11100, 10000, and 11001.
    Then, consider the second bit of the 7 remaining numbers: there are more 0 bits (4) than 1 bits (3), so keep only the 4 numbers with a 0 in the second position: 10110, 10111, 10101, and 10000.
    etc to the fifth position, there are an equal number of 0 bits and 1 bits (one each).
    So, to find the oxygen generator rating, keep the number with a 1 in that position: 10111.
    As there is only one number left, stop; the oxygen generator rating is 10111, or 23 in decimal.

    Then... the opposite for CO2
    There are fewer 0 bits (5) than 1 bits (7), so keep only the 5 numbers with a 0 in the first position: 00100, 01111, 00111, 00010, and 01010.
    In the third position, there are an equal number of 0 bits and 1 bits (one each). So, to find the CO2 scrubber rating, keep the number with a 0 in that position: 01010.
    As there is only one number left, stop; the CO2 scrubber rating is 01010, or 10 in decimal.
    """
    input_lines = get_input(day=3)
    line_length = len(input_lines[0])

    oxygen = 0
    co2 = 0
    oxygen_candidates = input_lines.copy()
    for column in range(0, line_length):
        oxygen_candidates = day_3_filter(oxygen_candidates, position=column, favour="1")
        if len(oxygen_candidates) == 1:
            print(f"{oxygen_candidates[0]=}")
            oxygen = int(oxygen_candidates[0], 2)
            break
    else:
        print(f"Oxygen failure")

    co2_candidates = input_lines
    for column in range(0, line_length):
        co2_candidates = day_3_filter(co2_candidates, position=column, favour="0")
        if len(co2_candidates) == 1:
            print(f"{co2_candidates[0]=}")
            co2 = int(co2_candidates[0], 2)
            break
    else:
        print(f"CO2 failure")

    print(f"{oxygen=}, {co2=}, {oxygen * co2=}")


def day_3_filter(candidates: List[str], position: int, favour: Literal["0", "1"]) -> List[str]:
    common_tuples = Counter([value[position] for value in candidates]).most_common()
    favour_index = -1 if favour == "0" else 0

    # Check equal value and use favour if so
    if common_tuples[0][1] == common_tuples[1][1]:
        bit_to_look_for = favour
    else:
        # Otherwise take the most/least common bit based on the favour
        bit_to_look_for = common_tuples[favour_index][0]

    return [value for value in candidates if value[position] == bit_to_look_for]


if __name__ == '__main__':
    print("Part 1:")
    day_3_part_1()
    print("\nPart 2:")
    day_3_part_2()
