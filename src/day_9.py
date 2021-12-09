from dataclasses import dataclass
from typing import List, Dict, Set, Iterable

from src.common import get_input

row_size: int = 0
number_of_rows: int = 0


@dataclass
class Node:
    value: int
    explored: bool
    x: int
    y: int

    @property
    def index(self):
        return get_index(self.x, self.y)

    def __hash__(self):
        return hash(self.index)


def day_9():
    # The input is a heightmap - find the lowest points in the sequence (which is lower than its adjacent neighbours)
    # The score "risk level" is the value + 1, summed
    input_lines = get_input(day=9)
    heightmap: List[List[int]] = [[int(val) for val in line.strip()] for line in input_lines]
    global row_size, number_of_rows
    row_size = len(heightmap[0])
    number_of_rows = len(input_lines)

    # We can calculate part 1 by taking all values in a basin and finding the lowest point.
    # The puzzle notes that all basins have a single low point.
    # I'm sure you can do some funky local minima calculus and DS algos here but I'm not smart.
    # What we'll do:
    # 1. Mark 9's as explored already to give us a stop/don't explore indication. They aren't included in any basin.
    # 2. Flag each value against the heightmap if it's been explored yet and its value (this is a Node).
    # 3. Starting with the first unexplored Node, calculate its neighbours and add to a local cache. This is our basin.
    # 4. Once all the nodes in the basin have been explored (no more neighbours), then the basin is complete.
    # 5. Iterate over the next unexplored node (outside of the basin just completed). Repeat steps 3-5 until everything is explored.
    # 6. For each completed basin, save it and calculate its minimum and size.
    # 7. The sum of each (minimum value + 1) gives our risk from part 1.
    # 8. The three largest basins' sizes, multiplied, gives the part 2 answer.

    all_nodes: Dict[int, Node] = {}
    for y, line in enumerate(heightmap):
        for x, val in enumerate(line):
            all_nodes[get_index(x, y)] = (Node(value=val, explored=True if val == 9 else False, x=x, y=y))

    basins: List[Set[Node]] = []
    for node in all_nodes.values():
        if not node.explored:
            basin = calculate_basin(all_nodes, node)
            basins.append(basin)

    # Sort the basins by size DESC.
    basins.sort(key=lambda b: len(b), reverse=True)
    low_points: List[int] = []
    for i, basin in enumerate(basins):
        low_point = get_low(basin)
        low_points.append(low_point)
        basin_size = len(basin)
        print(f"Basin #{i} analysed, it contained {basin_size} nodes. Its low point is {low_point}.")

    print("Part 1:")
    print(f"{low_points=}")
    risk = calculate_score(low_points)
    print(f"{risk=}")
    print("\nPart 2:")
    print(f"{len(basins[0])=} * {len(basins[1])=} * {len(basins[2])=} = {len(basins[0]) * len(basins[1]) * len(basins[2])}")


def calculate_basin(all_nodes: Dict[int, Node], first_node: Node) -> Set[Node]:
    basin: Set[Node] = {first_node}
    while True:
        unexplored_node = next((n for n in basin if not n.explored), None)
        if unexplored_node:
            new_neighbours = get_unexplored_neighbours(all_nodes, unexplored_node)  # This also sets node to explored
            basin.update(new_neighbours)
        else:
            break
    return basin


def get_unexplored_neighbours(all_nodes: Dict[int, Node], n: Node) -> Set[Node]:
    result = []
    if n.x != 0:
        result.append(all_nodes[get_index(n.x - 1, n.y)])
    if n.y != 0:
        result.append(all_nodes[get_index(n.x, n.y - 1)])
    if (n.x + 1) != row_size:
        result.append(all_nodes[get_index(n.x + 1, n.y)])
    if (n.y + 1) != number_of_rows:
        result.append(all_nodes[get_index(n.x, n.y + 1)])
    n.explored = True
    return {result for result in result if not result.explored}


def get_low(nodes: Iterable[Node]) -> int:
    return min([n.value for n in nodes])


def calculate_score(lows: List[int]) -> int:
    return sum(val + 1 for val in lows)


def get_index(x: int, y: int):
    return x + (y * row_size)


if __name__ == '__main__':
    day_9()
