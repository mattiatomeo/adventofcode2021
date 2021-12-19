import numpy as np

from typing import Tuple, List


def read_octopuses(file_path: str) -> np.array:
    with open(file_path, 'r') as f:
        return np.array([
            list(map(int, row.strip())) for row in f.readlines()
        ])


def propagate_energy_increase(octopuses_state: np.array):
    row, col = octopuses_state.shape
    covered_positions = set()

    def select_next_propagation_points(curr_propagation_state: np.array) -> List[Tuple[int, int]]:
        candidates = np.argwhere(curr_propagation_state >= 10)

        return list(
            filter(lambda pos: pos not in covered_positions, map(tuple, candidates))
        )

    flashed_pos = select_next_propagation_points(octopuses_state)
    while len(flashed_pos) != 0:
        for octopus in flashed_pos:
            row_neigh = slice(
                max(0, octopus[0] - 1),
                min(row - 1, octopus[0] + 1) + 1
            )
            col_neigh = slice(
                max(0, octopus[1] - 1),
                min(col - 1, octopus[1] + 1) + 1
            )

            octopuses_state[row_neigh, col_neigh] += 1
            covered_positions.add((octopus[0], octopus[1]))

        flashed_pos = select_next_propagation_points(octopuses_state)


def count_flashes_in_step(initial_octopuses_state: np.array, step: int) -> np.array:
    curr_state = initial_octopuses_state.copy()

    total_flashes = 0
    for _ in range(step):
        curr_state += 1
        propagate_energy_increase(curr_state)

        flashed_octopuses = np.argwhere(curr_state >= 10)
        curr_state[flashed_octopuses[:, 0], flashed_octopuses[:, 1]] = 0
        total_flashes += flashed_octopuses.shape[0]

    return total_flashes


def get_first_step_all_flashes(initial_octopuses_state: np.array) -> int:
    curr_step = 0
    curr_state = initial_octopuses_state.copy()

    def all_octopuses_flashes(curr_octopuses_state: np.array) -> bool:
        return not np.any(curr_octopuses_state)

    while not all_octopuses_flashes(curr_state):
        curr_state += 1
        curr_step += 1
        propagate_energy_increase(curr_state)

        flashed_octopuses = np.argwhere(curr_state >= 10)
        curr_state[flashed_octopuses[:, 0], flashed_octopuses[:, 1]] = 0

    return curr_step


def main():
    octopuses = read_octopuses('input.txt')
    test_matrix = read_octopuses('input_test.txt')

    assert count_flashes_in_step(test_matrix, 10) == 204
    assert count_flashes_in_step(octopuses, 100) == 1627

    assert get_first_step_all_flashes(test_matrix) == 195
    assert get_first_step_all_flashes(octopuses) == 329


if __name__ == '__main__':
    main()
