import numpy as np
from dataclasses import dataclass
from typing import Tuple, List, Generator

Segment = Tuple["Point", "Point"]


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def coords(self) -> Tuple[int, int]:
        return self.x, self.y

    def __add__(self, other):
        if not isinstance(other, Point):
            return NotImplemented

        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented

        return self.x == other.x and self.y == other.y


class Grid:
    def __init__(self, size: int):
        self.matrix = np.full((size, size), 0)

    def draw_line(self, segment: Segment):
        if segment[0].x == segment[1].x:
            self.draw_on_y_axis(segment)
        elif segment[0].y == segment[1].y:
            self.draw_on_x_axis(segment)
        else:
            self.draw_on_diagonal(segment)

    def draw_on_x_axis(self, segment: Segment):
        assert segment[0].y == segment[1].y

        x_start = min(segment[0].x, segment[1].x)
        x_end = max(segment[0].x, segment[1].x)

        self.matrix[segment[0].y, x_start:x_end + 1] += 1

    def draw_on_y_axis(self, segment: Segment):
        assert segment[0].x == segment[1].x

        y_start = min(segment[0].y, segment[1].y)
        y_end = max(segment[0].y, segment[1].y)

        self.matrix[y_start:y_end + 1, segment[0].x] += 1

    def draw_on_diagonal(self, segment: Segment):
        x_step_direction = 1 if segment[0].x < segment[1].x else -1
        y_step_direction = 1 if segment[0].y < segment[1].y else -1

        self.matrix[
            range(segment[0].y, segment[1].y + y_step_direction, y_step_direction),
            range(segment[0].x, segment[1].x + x_step_direction, x_step_direction)
        ] += 1

    def get_num_of_interception(self) -> int:
        flatten = self.matrix.flatten()
        return flatten[flatten > 1].shape[0]

    def reset(self):
        self.matrix.fill(0)


def read_segments() -> List[Segment]:
    def str_to_point(point_str: str) -> Point:
        return Point(*[int(coord) for coord in point_str.split(',')])

    def parse_row(line: str) -> Segment:
        points = line.strip().split(' -> ')

        return str_to_point(points[0]), str_to_point(points[1])

    def read_str_segments(lines: List[str]) -> Generator[Segment, None, None]:
        return (
            parse_row(row.strip()) for row in lines
        )

    with open('input.txt') as f:
        return [
            segment for segment in read_str_segments(f.readlines())
        ]


def is_straight(segment: Segment) -> bool:
    return (
        segment[0].x == segment[1].x
        or segment[0].y == segment[1].y
    )


def create_grid(segments: List[Segment]) -> Grid:
    def max_axis_value(seg: Segment):
        return max((seg[0].x, seg[0].y, seg[1].x, seg[1].y))

    shape = max(map(max_axis_value, segments)) + 1

    return Grid(shape)


if __name__ == '__main__':
    hydrothermal_vents = read_segments()
    grid = create_grid(hydrothermal_vents)

    for seg in (seg for seg in hydrothermal_vents if is_straight(seg)):
        grid.draw_line(seg)

    assert grid.get_num_of_interception() == 6666

    grid.reset()

    for seg in hydrothermal_vents:
        grid.draw_line(seg)

    assert grid.get_num_of_interception() == 19081
