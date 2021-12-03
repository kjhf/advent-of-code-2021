from src.common import get_input


def day_1(slider: int):
    input_lines = get_input(day=1)

    # Count the number of times the sum of measurements in this sliding window of (slider) increases from the previous sum
    # Part 1 is an increase one-by-one, part 2 is slider of 3.
    larger = 0
    for i in range(0, len(input_lines) - slider):  # Count back the slider amount
        this_el = 0
        next_el = 0
        for j in range(0, slider):
            this_el += int(input_lines[i + j])
            next_el += int(input_lines[i + j + 1])

        if next_el > this_el:
            larger += 1

    print(larger)


if __name__ == '__main__':
    print("Part 1:")
    day_1(1)
    print("\nPart 2:")
    day_1(3)
