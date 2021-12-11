import numpy as np

from typing import Callable, List


def read_crabs_positions() -> np.array:
    with open("input.txt", "r") as f:
        return list(map(int, f.readline().split(',')))


def find_cheapest_position(crabs_positions: List[int], distance: Callable[[int, int], int]) -> int:
    min_pos = min(crabs_positions)
    max_pos = max(crabs_positions)

    def fuel_consumption(position: int) -> int:
        return sum(distance(crab, position) for crab in crabs_positions)

    return min(fuel_consumption(pos) for pos in range(min_pos, max_pos + 1))


if __name__ == '__main__':
    crabs_positions = read_crabs_positions()
    test_positions = np.array([16, 1, 2, 0, 4, 2, 7, 1, 2, 14])

    def unit_distance(crab_position, position):
        return abs(crab_position - position)

    assert find_cheapest_position(test_positions, unit_distance) == 37
    assert find_cheapest_position(crabs_positions, unit_distance) == 328318

    def incremental_distance(crab_position, position):
        dist = abs(crab_position - position)

        return (dist * (dist + 1)) / 2

    assert find_cheapest_position(test_positions, incremental_distance) == 168
    assert find_cheapest_position(crabs_positions, incremental_distance) == 89791146
