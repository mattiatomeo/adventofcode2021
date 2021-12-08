import numpy as np

from typing import List, Any


def load_initial_fishes() -> List[int]:
    with open('input.txt', 'r') as f:
        return [int(time_before_first_child) for time_before_first_child in f.readline().split(',')]


def flatten(seq: List[List[Any]]) -> List[Any]:
    return [item for subseq in seq for item in subseq]


def compute_population_after_days(initial_fishes: List[int], days: int) -> int:
    fish_of_age = np.full(10, 0)

    for fish in initial_fishes:
        fish_of_age[fish] += 1

    for _ in range(days):
        fish_of_age = np.roll(fish_of_age, -1)
        new_fishes = fish_of_age[9]
        fish_of_age[8] += new_fishes
        fish_of_age[6] += new_fishes
        fish_of_age[9] = 0

    return fish_of_age.sum()


if __name__ == '__main__':
    assert compute_population_after_days([3, 4, 3, 1, 2], 18) == 26
    assert compute_population_after_days([3, 4, 3, 1, 2], 80) == 5934
    assert compute_population_after_days([3, 4, 3, 1, 2], 256) == 26984457539

    initial_population = load_initial_fishes()

    assert compute_population_after_days(initial_population, 80) == 361169
    assert compute_population_after_days(initial_population, 256) == 1634946868992


