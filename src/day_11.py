from dataclasses import dataclass
from typing import List, Dict, Set

from src.common import get_input

row_size: int = 0
number_of_rows: int = 0


@dataclass
class Octo:
    value: int
    flash_calculated: bool
    x: int
    y: int

    @property
    def index(self):
        return get_index(self.x, self.y)

    @property
    def needs_calc(self):
        return (not self.flash_calculated) and self.value > 9

    def __hash__(self):
        return hash(self.index)

    def step(self) -> 'Octo':
        self.flash_calculated = False
        if self.value > 9:
            self.value = 0

        self.value += 1
        return self


def day_11():
    # Part 1: 100 octopuses arranged neatly in a 10 by 10 grid. Each has an energy [0-9].
    # In one step, each increases by 1. At >9 flashes, all adjacent (cardinal and diagonals) ++. Repeat.
    # All flashes reset to 0.
    # A lot of this can be built off of the day 9 code ...
    # Part 1: How many total flashes are there after 100 steps?
    # Part 2: What is the first step where all the Octos synchronise?
    input_lines = get_input(day=11)
    octos: List[List[int]] = [[int(val) for val in line.strip()] for line in input_lines]
    global row_size, number_of_rows
    row_size = len(octos[0])
    number_of_rows = len(input_lines)

    # Transform the input into Nodes
    all_nodes: Dict[int, Octo] = {}
    for y, line in enumerate(octos):
        for x, val in enumerate(line):
            all_nodes[get_index(x, y)] = (Octo(value=val, flash_calculated=False, x=x, y=y))

    print(f"{run_sim(all_nodes)=}")


def run_sim(all_nodes: Dict[int, Octo]) -> int:
    result_flashes = 0
    for step in range(0, 10000):
        flashes_this_step = 0

        # First, make a dumb increment of all nodes and reset its flash calculated flag.
        all_nodes = {k: (v.step()) for k, v in all_nodes.items()}

        # For each Octo that's flashing
        while True:
            flashing = {k: v for k, v in all_nodes.items() if v.needs_calc}
            if flashing:
                flashes_this_step += len(flashing)
                for flash_node in flashing.values():
                    neighbours = get_neighbours(all_nodes, flash_node)
                    # Increment
                    for neighbour in neighbours:
                        neighbour.value += 1
                    flash_node.flash_calculated = True
            else:
                break

        result_flashes += flashes_this_step
        if step == 99:
            print("-----------------------------------")
            print("Part 1:")
        print(f"Step {step+1} calculated, {flashes_this_step=}, for a total {result_flashes=}.")
        if step == 99:
            print("-----------------------------------")

        # Part 2, perform synchro checks past step 100.
        if step > 100:
            if flashes_this_step == (row_size * number_of_rows):
                # Synced!
                print(f"Step {step + 1} -- all Octos in sync. Stopping program.")
                assert all((v.value > 9 for v in all_nodes.values())), \
                    f"Expected all values above 9 with {(row_size * number_of_rows)=} flashes this step."
                break

    return result_flashes


def get_neighbours(all_nodes: Dict[int, Octo], n: Octo) -> Set[Octo]:
    result = set()
    has_north = n.y != 0
    has_east = (n.x + 1) != row_size
    has_south = (n.y + 1) != number_of_rows
    has_west = n.x != 0

    # N
    if has_north:
        result.add(all_nodes[get_index(n.x, n.y - 1)])
    # NE
    if has_north and has_east:
        result.add(all_nodes[get_index(n.x + 1, n.y - 1)])
    # E
    if has_east:
        result.add(all_nodes[get_index(n.x + 1, n.y)])
    # SE
    if has_south and has_east:
        result.add(all_nodes[get_index(n.x + 1, n.y + 1)])
    # S
    if has_south:
        result.add(all_nodes[get_index(n.x, n.y + 1)])
    # SW
    if has_south and has_west:
        result.add(all_nodes[get_index(n.x - 1, n.y + 1)])
    # W
    if has_west:
        result.add(all_nodes[get_index(n.x - 1, n.y)])
    # NW
    if has_north and has_west:
        result.add(all_nodes[get_index(n.x - 1, n.y - 1)])
    return result


def get_index(x: int, y: int):
    return x + (y * row_size)


if __name__ == '__main__':
    day_11()
