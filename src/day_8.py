from collections import Counter
from typing import List, Dict, Set

from src.common import get_input


def day_8():
    # Puzzle input is ten unique signal patterns (0-9), | delimiter, then a four digit output value.
    # The connections are scrambled per line in both input and output. We have to decode them...
    input_lines = get_input(day=8)
    input_dict = {(line.split('|')[0].strip()): (line.split('|')[1].strip()) for line in input_lines}

    c = Counter()
    part_2_sum = 0
    for inp, output in input_dict.items():
        # Map the inputs
        mapping_dict = build_map(inp.split(' '))

        # Then, count the digits according to their map.
        line_display = ''
        for digit in output.split(' '):
            result = mapping_dict[''.join(sorted(digit))]

            # Add the digit to our current display
            line_display += result.__str__()

            # Count the digit for Part 1
            c[result] += 1
        part_2_sum += int(line_display)

    print(f"{c[1]=}, {c[4]=}, {c[7]=}, {c[8]=}, Part 1 sum={c[1] + c[4] + c[7] + c[8]}")
    print(f"{part_2_sum=}")


def build_map(inp: List[str]) -> Dict[str, int]:
    """
    # DIGIT  |  LEN  |  SHARED?
    #   0    |   6   |  0,6,9
    #   1    |   2   |    -
    #   2    |   5   |  2,3,5
    #   3    |   5   |  2,3,5
    #   4    |   4   |    -
    #   5    |   5   |  2,3,5
    #   6    |   6   |  0,6,9
    #   7    |   3   |    -
    #   8    |   7   |    -
    #   9    |   6   |  0,6,9
    #
    # So we can immediately work out 1, 4, 7, 8.
    # If a number contains 7 it must contain 1. The only numbers that don't contain both are 1 and 4 (but we know them).
    # The set of 4 will determine the rest...
    # From this we can work out what the other digits are:
    # DIGIT  | DERIVE?
    #   3    |  len 5 and contains 7 but NOT 4.
    #   0    |  len 6 and contains 7 but NOT 3 and 4.
    #   9    |  len 6 contains 3 and 4.
    #   6    |  len 6, NOT 1,3,4.
    # 8 - 6 = position C
    #   2    |  len 5 contains C (not 1(7),4)
    #   5    |  len 5 does not contain C (not 1(7),4)
    :param inp: List of input strings to build the map
    :return: The mapping from string to digit
    """
    char_set: Dict[int, Set[str]] = {}
    input_sets = [set(i) for i in inp]

    # Search for 1, 4, 7, 8 in the inp list.
    for digit_set in input_sets.copy():
        if len(digit_set) == 2:  # if it's a '1'
            char_set[1] = digit_set
            input_sets.remove(digit_set)
        elif len(digit_set) == 4:  # if it's a '4'
            char_set[4] = digit_set
            input_sets.remove(digit_set)
        elif len(digit_set) == 3:  # if it's a '7'
            char_set[7] = digit_set
            input_sets.remove(digit_set)
        elif len(digit_set) == 7:  # if it's a '8'
            char_set[8] = digit_set
            input_sets.remove(digit_set)

    # Search for a 3.
    matched = next((digit_set for digit_set in input_sets
                   if len(digit_set) == 5
                   and char_set[7].issubset(digit_set)
                   and not char_set[4].issubset(digit_set)), None)
    assert matched, f"Couldn't find the digit sequence for 3... {inp=}"
    char_set[3] = matched
    input_sets.remove(matched)

    # Search for a 0.
    matched = next((digit_set for digit_set in input_sets
                   if len(digit_set) == 6
                   and char_set[7].issubset(digit_set)
                   and not char_set[3].issubset(digit_set)
                   and not char_set[4].issubset(digit_set)), None)
    assert matched, f"Couldn't find the digit sequence for 0... {inp=}"
    char_set[0] = matched
    input_sets.remove(matched)

    # Search for a 9.
    matched = next((digit_set for digit_set in input_sets
                   if len(digit_set) == 6
                   and char_set[3].issubset(digit_set)
                   and char_set[4].issubset(digit_set)), None)
    assert matched, f"Couldn't find the digit sequence for 9... {inp=}"
    char_set[9] = matched
    input_sets.remove(matched)

    # Search for a 6.
    matched = next((digit_set for digit_set in input_sets
                   if len(digit_set) == 6
                   and not char_set[1].issubset(digit_set)
                   and not char_set[3].issubset(digit_set)
                   and not char_set[4].issubset(digit_set)), None)
    assert matched, f"Couldn't find the digit sequence for 6... {inp=}"
    char_set[6] = matched
    input_sets.remove(matched)

    # Get position C
    position_c = next(iter(char_set[8] - char_set[6]))

    # Search for a 2.
    matched = next((digit_set for digit_set in input_sets
                   if len(digit_set) == 5
                   and position_c in digit_set), None)
    assert matched, f"Couldn't find the digit sequence for 2... {inp=}"
    char_set[2] = matched
    input_sets.remove(matched)

    # Search for a 5.
    matched = next((digit_set for digit_set in input_sets
                   if len(digit_set) == 5
                   and position_c not in digit_set), None)
    assert matched, f"Couldn't find the digit sequence for 5... {inp=}"
    char_set[5] = matched
    input_sets.remove(matched)

    # Verify we got everything
    assert len(input_sets) == 0, f"There are still inputs to process! {input_sets=}"
    assert all(el in char_set.keys() for el in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    # Return as a dict keyed by the ordered char list (str), and the corresponding digit value
    return {''.join(sorted(list(string))): digit for digit, string in char_set.items()}


if __name__ == '__main__':
    day_8()
