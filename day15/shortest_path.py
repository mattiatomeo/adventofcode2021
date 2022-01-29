from bisect import bisect
from dataclasses import dataclass, field
import itertools
import math
from typing import Iterator, List


@dataclass(frozen=True)
class CavePosition:
    row: int
    col: int


@dataclass(frozen=True)
class PriorityQueueEntry:
    position: CavePosition
    risk_from_start: int


@dataclass
class PriorityQueue:
    items: List[PriorityQueueEntry] = field(init=False, default_factory=list)

    def pop_first(self) -> PriorityQueueEntry:
        return self.items.pop(0)

    def add_item(self, entry: PriorityQueueEntry):
        pos = bisect(self.items, entry.risk_from_start, key=lambda item: item.risk_from_start)

        self.items.insert(pos, entry)

    def update_risk_level(self, to_update: CavePosition, new_risk_level: int):
        self.drop_if_exists(to_update)
        self.add_item(PriorityQueueEntry(to_update, new_risk_level))

    def drop_if_exists(self, to_remove: CavePosition):
        for pos in range(len(self.items)):
            if self.items[pos].position == to_remove:
                break

        if pos < len(self.items):
            del self.items[pos]


    @property
    def empty(self) -> bool:
        return len(self.items) == 0


@dataclass(frozen=True)
class RiskMap:
    risk_level: List[List[int]]

    def get_neighbors(self, pos: CavePosition) -> Iterator[CavePosition]:
        neighbor_pos = (
            (pos.row, pos.col - 1),
            (pos.row, pos.col + 1),
            (pos.row - 1, pos.col),
            (pos.row + 1, pos.col)
        )

        for candidate in neighbor_pos:
            if (
                0 <= candidate[0] < self.shape[0]
                and 0 <= candidate[1] < self.shape[1]
            ):
                yield CavePosition(*candidate)

    def get_risk_level(self, pos: CavePosition) -> int:
        return self.risk_level[pos.row][pos.col]

    def get_all_positions(self) -> Iterator[CavePosition]:
        cols = range(len(self.risk_level[0]))
        rows = range(len(self.risk_level))

        return list(
            map(lambda pos: CavePosition(*pos), itertools.product(rows, cols))
        )

    @property
    def shape(self):
        return len(self.risk_level[0]), len(self.risk_level)


def read_map(filepath: str) -> RiskMap:
    with open(filepath, 'r') as fp:
        return RiskMap([
            list(map(int, row.strip())) for row in fp.readlines()
        ])


def get_shortest_risk(risk_map: RiskMap) -> int:
    start = CavePosition(0, 0)

    risk_from_start = {start: 0}

    vertex_queue = PriorityQueue()
    vertex_to_traverse = set()

    for position in risk_map.get_all_positions():
        if position != start:
            risk_from_start[position] = math.inf
            vertex_to_traverse.add(position)

        vertex_queue.add_item(PriorityQueueEntry(position, risk_from_start[position]))


    while not vertex_queue.empty:
        curr_pos = vertex_queue.pop_first()

        curr_cave = curr_pos.position
        for neighbor in (pos for pos in risk_map.get_neighbors(curr_cave) if pos in vertex_to_traverse):
            if neighbor == start:
                continue

            risk_from_curr = risk_from_start[curr_cave] + risk_map.get_risk_level(neighbor)

            if risk_from_curr < risk_from_start[neighbor]:
                risk_from_start[neighbor] = risk_from_curr

                vertex_queue.update_risk_level(neighbor, risk_from_curr)

            vertex_to_traverse.remove(neighbor)

    destination = CavePosition(risk_map.shape[0] - 1, risk_map.shape[1] -1)
    return risk_from_start[destination]

def main():
    test_risk_map = read_map('input_test.txt')
    risk_map = read_map('input.txt')

    assert get_shortest_risk(test_risk_map) == 40
    assert get_shortest_risk(risk_map) == 702

if __name__ == "__main__":
    main()
