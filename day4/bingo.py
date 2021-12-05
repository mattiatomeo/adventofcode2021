import enum
from enum import auto

import numpy as np
import itertools

from typing import List, Tuple, Dict, Optional, Set

BingoNumbers = List[int]
RowPosition = int
ColPosition = int


class BingoWinAxis(enum.Enum):
    NONE = auto()
    ROW = auto()
    COL = auto()


class Board:
    def __init__(self, board_numbers: np.array):
        self.numbers = board_numbers
        self.unmarked = set(board_numbers.flatten())

        self.numbers_on_axis = self.numbers.shape[0]

        self.drawn_numbers_in_row = {
            row: 0 for row in range(self.numbers_on_axis)
        }  # type: Dict[RowPosition, int]
        self.drawn_numbers_in_col = {
            col: 0 for col in range(self.numbers_on_axis)
        }  # type: Dict[ColPosition, int]

        self.number_position = {
            self.numbers[row, col]: (row, col)
            for row, col in itertools.product(range(self.numbers_on_axis), repeat=2)
        }  # type: Dict[int, Tuple[RowPosition, ColPosition]]

        self.winner = False

    def drawn_number(self, drawn: int):
        """
        Drawn a number and mark the board, if the number is included inside the board.

        :param drawn: new number drawn during the game
        """
        if drawn not in self.number_position:
            return

        row, col = self.number_position[drawn]
        self.drawn_numbers_in_row[row] += 1
        self.drawn_numbers_in_col[col] += 1

        self.unmarked.remove(drawn)

        if (self.drawn_numbers_in_row[row] == self.numbers_on_axis
                or self.drawn_numbers_in_col[col] == self.numbers_on_axis):
            self.winner = True

    def bingo(self) -> bool:
        return self.winner

    def get_unmarked(self) -> Set[int]:
        return set(self.unmarked)

    def __str__(self):
        return str(self.numbers)


def read_numbers_and_boards() -> Tuple[BingoNumbers, Set[Board]]:
    def init_matrix(mtx: List[str]) -> Board:
        return Board(np.array([
            [int(num) for num in row.split()] for row in mtx
        ]))

    with open("input.txt", "r") as f:
        lines = [line.strip() for line in f.readlines()]
        numbers = [int(num) for num in lines[0].split(",")]
        boards = set(
            init_matrix(lines[curr_pos:curr_pos + 5]) for curr_pos in range(2, len(lines), 6)
        )

        return numbers, boards


def step_1() -> Optional[int]:
    numbers, boards = read_numbers_and_boards()

    while len(numbers) > 0:
        drawn = numbers.pop(0)
        winner_boards = set()
        for board in boards:
            board.drawn_number(drawn)

            if board.bingo():
                winner_boards.add(board)
                return sum(board.get_unmarked()) * drawn

    return None


def step_2() -> Optional[int]:
    numbers, boards = read_numbers_and_boards()

    while len(numbers) > 0:
        drawn = numbers.pop(0)
        winner_boards = set()
        for board in boards:
            board.drawn_number(drawn)

            if board.bingo():
                winner_boards.add(board)

        boards -= winner_boards

        if len(boards) == 0:
            return sum(winner_boards.pop().get_unmarked()) * drawn

    return None


if __name__ == '__main__':
    assert step_1() == 2745
    assert step_2() == 6594
