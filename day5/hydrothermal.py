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


class Matrix:
    def __init__(self, size: int):
        self.mtx = np.full((size, size), 0)

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

        self.mtx[segment[0].y, x_start:x_end + 1] += 1

    def draw_on_y_axis(self, segment: Segment):
        assert segment[0].x == segment[1].x

        y_start = min(segment[0].y, segment[1].y)
        y_end = max(segment[0].y, segment[1].y)

        self.mtx[y_start:y_end + 1, segment[0].x] += 1

    def draw_on_diagonal(self, segment: Segment):
        x_step = 1 if segment[0].x < segment[1].x else -1
        y_step = 1 if segment[0].y < segment[1].y else -1

        step = Point(x_step, y_step)
        curr = Point(*segment[0].coords())
        end = Point(*segment[1].coords()) + Point(x_step, y_step)
        while curr != end:
            self.mtx[curr.y, curr.x] += 1
            curr += step

    def get_num_of_interception(self) -> int:
        flatten = self.mtx.flatten()
        return flatten[flatten > 1].shape[0]

    def reset(self):
        self.mtx.fill(0)


def read_segments(keep_only_straight_lines: bool) -> List[Segment]:
    def str_to_point(point_str: str) -> Point:
        return Point(*[int(coord) for coord in point_str.split(',')])

    def is_straight(segment: Segment) -> bool:
        return (
            segment[0].x == segment[1].x
            or segment[0].y == segment[1].y
        )

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
            if not keep_only_straight_lines or is_straight(segment)
        ]


if __name__ == '__main__':
    mtx = Matrix(1000)

    for seg in read_segments(True):
        mtx.draw_line(seg)

    assert mtx.get_num_of_interception() == 6666

    mtx.reset()

    for seq in read_segments(False):
        mtx.draw_line(seq)

    assert mtx.get_num_of_interception() == 19081
