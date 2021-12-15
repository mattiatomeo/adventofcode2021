import numpy as np


def read_input(file_path: str) -> np.array:
    with open(file_path, 'r') as f:
        return np.array([
            list(map(int, row.strip())) for row in f.readlines()
        ])


def find_low_points(heatmap: np.array):
    height_sum = 0
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

    return height_sum


def step_1(heatmap: np.array) -> int:
    low_points_pos = list(find_low_points(heatmap))
    pos = (
        np.array([x for x, _ in low_points_pos]),
        np.array([y for _, y in low_points_pos])
    )

    return (heatmap[pos] + 1).sum()


if __name__ == '__main__':
    heatmap = read_input('input.txt')

    assert step_1(heatmap) == 502
