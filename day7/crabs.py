import numpy as np

from typing import Callable


def read_crabs_positions() -> np.array:
    with open("input.txt", "r") as f:
        return np.array([int(pos) for pos in f.readline().split(',')])


def find_cheapest_position(crabs_positions: np.array, distance: Callable[[int, int], int]) -> int:
    curr_position = crabs_positions.min()

    vect_dist_f = np.vectorize(distance)

    curr_pos_value = vect_dist_f(crabs_positions, curr_position).sum()
    curr_position += 1
    while curr_position < crabs_positions.max():
        next_position_value = vect_dist_f(crabs_positions, curr_position).sum()

        if next_position_value > curr_pos_value:
            break

        curr_pos_value = next_position_value
        curr_position += 1

    return curr_pos_value


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
