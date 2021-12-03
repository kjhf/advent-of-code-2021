from src.common import get_input


def day_2_part_1():
    input_lines = get_input(day=2)
    position = 0
    depth = 0
    for string in input_lines:
        parts = string.partition(" ")
        direction = parts[0]
        amount = int(parts[2])

        if direction.lower() == "forward":
            position += amount
        elif direction.lower() == "down":
            depth += amount
        elif direction.lower() == "up":
            depth -= amount
        elif direction.lower() == "backward":  # not needed but my OCD cries if I omit it
            position -= amount

    print(f"{position=}, {depth=}, {position*depth=}")


def day_2_part_2():
    input_lines = get_input(day=2)
    position = 0
    depth = 0
    aim = 0
    for string in input_lines:
        parts = string.partition(" ")
        direction = parts[0]
        amount = int(parts[2])

        if direction.lower() == "forward":
            position += amount
            depth += aim * amount
        elif direction.lower() == "down":
            aim += amount
        elif direction.lower() == "up":
            aim -= amount

    print(f"{position=}, {depth=}, {position*depth=}")


if __name__ == '__main__':
    day_2_part_1()
    day_2_part_2()
