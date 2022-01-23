from dataclasses import dataclass
import itertools
import math
from typing import Iterator, List

from pip import main


@dataclass(frozen=True)
class CavePosition:
    row: int
    col: int


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

    vertex_to_traverse = {}

    for position in risk_map.get_all_positions():
        if position != start:
            risk_from_start[position] = math.inf

        vertex_to_traverse[position] = risk_from_start[position]

    while len(vertex_to_traverse) != 0:
        curr_pos = min(vertex_to_traverse.keys(), key=vertex_to_traverse.__getitem__)

        del vertex_to_traverse[curr_pos]

        for neighbor in (pos for pos in risk_map.get_neighbors(curr_pos) if pos in vertex_to_traverse):
            if neighbor == start:
                continue

            risk_from_curr = risk_from_start[curr_pos] + risk_map.get_risk_level(neighbor)

            if risk_from_curr < risk_from_start[neighbor]:
                risk_from_start[neighbor] = risk_from_curr

                vertex_to_traverse[neighbor] = risk_from_curr


    destination = CavePosition(risk_map.shape[0] - 1, risk_map.shape[1] -1)
    return risk_from_start[destination]

def main():
    test_risk_map = read_map('input_test.txt')
    risk_map = read_map('input.txt')

    assert get_shortest_risk(test_risk_map) == 40
    assert get_shortest_risk(risk_map) == 702

if __name__ == "__main__":
    main()
