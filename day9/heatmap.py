import numpy as np
from typing import Set
from collections import namedtuple


def read_input(file_path: str) -> np.array:
    with open(file_path, 'r') as f:
        return np.array([
            list(map(int, row.strip())) for row in f.readlines()
        ])


def find_low_points(heatmap: np.array):
    row_count, col_count = heatmap.shape
    for row in range(row_count):
        start_row = max(0, row - 1)
        end_row = min(row_count - 1, row + 1) + 1
        for col in range(col_count):
            start_col = max(0, col - 1)
            end_col = min(col_count - 1, col + 1) + 1

            value = heatmap[row, col]
            if value == heatmap[start_row:end_row, start_col:end_col].min():
                yield row, col


def step_1(heatmap: np.array) -> int:
    low_points_pos = list(find_low_points(heatmap))
    pos = (
        np.array([x for x, _ in low_points_pos]),
        np.array([y for _, y in low_points_pos])
    )

    return (heatmap[pos] + 1).sum()


HeatMapPosition = namedtuple('HeatMapPosition', ['x', 'y'])


def step_2(heatmap: np.array) -> int:
    rows, cols = heatmap.shape
    checked_pos = set()

    def uncovered_points(curr_position: HeatMapPosition, already_detected: set) -> Set[HeatMapPosition]:
        positions = [
            HeatMapPosition(curr_position.x, max(0, curr_position.y - 1)),
            HeatMapPosition(curr_position.x, min(cols - 1, curr_position.y + 1)),
            HeatMapPosition(max(0, curr_position.x - 1), curr_position.y),
            HeatMapPosition(min(rows - 1, curr_position.x + 1), curr_position.y)
        ]

        return set(filter(lambda pos: pos not in checked_pos and pos not in already_detected, positions))

    def belongs_to_basins(height: HeatMapPosition, curr_position: HeatMapPosition) -> bool:
        return heatmap[height] >= heatmap[curr_position] + 1 and heatmap[height] != 9

    def basin_size(low_point: HeatMapPosition) -> int:
        position_to_verify = {low_point}
        size = 1

        while len(position_to_verify) > 0:
            curr = position_to_verify.pop()

            checked_pos.add(curr)

            uncovered_neighbors = set(
                filter(lambda neighbor: belongs_to_basins(neighbor, curr), uncovered_points(curr, position_to_verify)))

            size += len(uncovered_neighbors)

            position_to_verify |= uncovered_neighbors

        return size

    low_points = map(lambda point: HeatMapPosition(*point), find_low_points(heatmap))
    basins_size = sorted(map(basin_size, low_points), reverse=True)

    return basins_size[0] * basins_size[1] * basins_size[2]


if __name__ == '__main__':
    heatmap = read_input('input.txt')
    example = read_input('input_test.txt')

    assert step_1(example) == 15
    assert step_2(example) == 1134
    assert step_1(heatmap) == 502
    assert step_2(heatmap) == 1330560