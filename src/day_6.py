from collections import Counter

from src.common import get_input


def day_6():
    # Each lanternfish creates a new lanternfish once every 7 days.
    # Model each fish as a single number that represents the number of days until it creates a new lantern-fish.
    # 0 is a valid value and produces offspring the following day. Each newborn has two more days for its first cycle.
    # e.g. internal timer would reset to 6, and it would create a new lanternfish with an internal timer of 8.
    # The input list are the ages of several hundred nearby lanternfish.
    # Initial state: 3,4,3,1,2
    # After  1 day:  2,3,2,0,1
    # After  2 days: 1,2,1,6,0,8; etc
    # In summary >>
    # Each day, a 0 becomes a 6 and adds a new 8 to the end of the list,
    # while each other number decreases by 1 if it was present at the start of the day.
    input_lines = get_input(day=6)
    # The obvious answer would be to make a list and append to it, but after an exponential increase,
    # your computer would die. So make a Counter from the input array instead ...
    ages = Counter([int(age) for age in input_lines[0].split(',') if age])
    run_for_days(ages=ages, days=256)


def run_for_days(ages: Counter, days: int):
    for day in range(0, days):
        ages = run_day(ages)
        print(f"Population after {day+1} days: {sum(ages.values())}")


def run_day(ages: Counter) -> Counter:
    """
    Create a new Counter based on the ages for this day.
    Each age takes the previous age, and anything on 0 becomes 6 (the parent) and 8 (the offspring)
    """
    to_add = ages.get(0, 0)
    new = Counter(
        {
            8: to_add,
            7: ages.get(8, 0),
            6: (ages.get(7, 0) + to_add),
            5: ages.get(6, 0),
            4: ages.get(5, 0),
            3: ages.get(4, 0),
            2: ages.get(3, 0),
            1: ages.get(2, 0),
            0: ages.get(1, 0),
        }
    )
    return new


if __name__ == '__main__':
    day_6()
