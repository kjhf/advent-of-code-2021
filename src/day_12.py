from collections import Counter
from dataclasses import dataclass
from typing import List, Dict, Literal

from src.common import get_input


@dataclass
class Node:
    label: str

    @property
    def is_small(self):
        return self.label.islower()

    def __str__(self):
        return self.label

    def __hash__(self):
        return hash(self.label)


@dataclass
class Edge:
    source: Node
    destination: Node

    def __str__(self):
        return f"{self.source.label}-{self.destination.label}"

    def __hash__(self):
        return hash(self.__str__())


class Journey:
    def __init__(self, nodes: List[Node] = None):
        self.nodes = nodes or []

    def can_travel_part_1(self, destination: Node) -> bool:
        return True if (not destination.is_small) or (destination not in self.nodes) else False

    def can_travel_part_2(self, destination: Node) -> bool:
        return True if ((not destination.is_small)
                        or (destination not in self.nodes)
                        or (True
                            #  A single small cave can be visited at most, twice, but not the start or end cave.
                            and (destination.label != 'start')
                            and (destination.label != 'end')
                            and (not self._has_small_cave_travelled_twice())
                            )
                        ) else False

    def _has_small_cave_travelled_twice(self) -> bool:
        small_caves = [n for n in self.nodes if n.is_small]
        c = Counter(small_caves)
        return c.most_common(1)[0][1] >= 2  # Get the most common, first [0], its count, is >= 2.

    def do_travel(self, destination: Node) -> 'Journey':
        return Journey(self.nodes + [destination])

    def is_at_end(self) -> bool:
        return self.nodes[-1].label == 'end'

    def __str__(self):
        return ','.join(n.label for n in self.nodes)


def day_12():
    input_lines = get_input(day=12)

    # The input is a list of connecting paths, split by -.
    # Count the unique routes from start to end via any link. Small caves (lowercase letters) cannot be re-entered.
    # Kinda feels like a dijkstras algo problem to me, or even a GA AI, but part 1 just wants
    # "How many paths through this cave system are there that visit small caves at most once?"

    # First we'll convert our input into edges and nodes
    edges = set()
    for line in input_lines:
        parts = line.partition('-')
        source = Node(parts[0])
        destination = Node(parts[2])
        edges.add(Edge(source, destination))
        # Also assume we can travel the other way.
        edges.add(Edge(destination, source))
    edges_by_source: Dict[Node, List[Edge]] = {}
    for e in edges:
        edges_by_source.setdefault(e.source, []).append(e)

    start_node = next((ed.source for ed in edges if ed.source.label == 'start'))
    do_the_thing(start_node, edges_by_source, 1)
    print("\n\n")
    do_the_thing(start_node, edges_by_source, 2)


def do_the_thing(start: Node, edges_by_source: Dict[Node, List[Edge]], puzzle_part: Literal[1, 2]):
    print(f"PART {puzzle_part}")
    journeys = travel_all(Journey(), start, edges_by_source, puzzle_part)
    print(f"Total routes: {len(journeys)}")

    # Filter anything that didn't end up at the end.
    finished_journeys = list(filter(lambda j: j.is_at_end(), journeys))

    # Sort for niceties.
    finished_journeys.sort(key=lambda j: len(j.nodes), reverse=True)
    print(f"Total finished journeys: {len(finished_journeys)}")
    print(f"Most nodes: {finished_journeys[0].__str__()} ({len(finished_journeys[0].nodes)} nodes)")
    print(f"Least nodes: {finished_journeys[-1].__str__()} ({len(finished_journeys[-1].nodes)} nodes)")


def travel_all(journey: Journey, current: Node, edges_by_source: Dict[Node, List[Edge]], puzzle_part: Literal[1, 2]) -> List[Journey]:
    result = []

    journey = journey.do_travel(current)
    if journey.is_at_end():
        # That's great.
        result.append(journey)
        return result

    # If we're too deep, bail.
    if len(journey.nodes) > 30:
        result.append(journey)
        return result

    # Else start recursing ...
    if puzzle_part == 1:
        available_routes = list(filter(lambda e: journey.can_travel_part_1(e.destination), edges_by_source[current]))
    elif puzzle_part == 2:
        available_routes = list(filter(lambda e: journey.can_travel_part_2(e.destination), edges_by_source[current]))
    else:
        assert False, "Unknown can_travel rules."
    if available_routes:
        for edge in available_routes:
            result.extend(travel_all(journey, edge.destination, edges_by_source, puzzle_part))
    else:
        # Nothing valid to travel to.
        result.append(journey)
    return result


if __name__ == '__main__':
    day_12()
