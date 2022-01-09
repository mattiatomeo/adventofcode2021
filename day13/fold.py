import dataclasses
import numpy as np
import re
from collections import namedtuple, Counter

from enum import Enum, auto


class FoldDirection(Enum):
    X = auto()
    Y = auto()

    @staticmethod
    def from_string(ch: str) -> 'FoldDirection':
        match ch.upper():
            case 'X':
                return FoldDirection.X
            case 'Y':
                return FoldDirection.Y
            case _:
                raise ValueError(f"Unknown value {ch}")


@dataclasses.dataclass(frozen=True)
class FoldOp:
    pos: int
    direction: FoldDirection

    def __str__(self) -> str:
        return f"{self.direction}={self.pos}"


Input = namedtuple('Input', ['paper', 'fold_ops'])


def read_input(filepath: str) -> Input:
    with open(filepath, 'r') as fp:
        dot_positions = []
        while ((row := fp.readline()) != '\n'):
            dot_positions.append(tuple(map(int, row.strip().split(','))))
        
        fold_operations = []
        while ((row := fp.readline()) != ''):
            matching = re.match(r"fold along (?P<direction>[xy])=(?P<pos>\d+)", row).groupdict()
            direction = FoldDirection.from_string(matching['direction'])
            pos = int(matching['pos'])

            fold_operations.append(FoldOp(pos, direction))
        

        dot_positions_array = np.array(dot_positions)
        
        paper = np.full(dot_positions_array.max(axis=0) + 1, '.').transpose()

        paper[dot_positions_array[:, 1], dot_positions_array[:, 0]] = '#'
        
        return Input(paper, fold_operations)


def fold_up(paper: np.ndarray, pos: int) -> np.ndarray:
    row_count = max(pos, paper.shape[0] - pos - 1)

    folded_paper = np.full((row_count, paper.shape[1]), '.')

    first_half = paper[:pos, :]
    
    start_position_for_merge = row_count - pos
    folded_paper[start_position_for_merge:, :] = first_half

    second_half = paper[(pos + 1):, :]
    for col in range(second_half.shape[0]):
        for row in range(second_half.shape[1]):
            idx = (col, row)
            position_to_update = (
                - col - 1, row
            )
            if second_half[idx] == '#':
                folded_paper[position_to_update] = '#'
    
    return folded_paper


def fold_left(paper: np.ndarray, pos: int) -> np.ndarray:
    col_count = max(pos, paper.shape[1] - pos - 1)

    folded_paper = np.full((paper.shape[0], col_count), '.')

    first_half = paper[:, :pos]
    
    start_position_for_merge = col_count - pos
    folded_paper[:, start_position_for_merge:] = first_half

    second_half = paper[:, (pos + 1):]
    for col in range(second_half.shape[0]):
        for row in range(second_half.shape[1]):
            idx = (col, row)
            position_to_update = (
                col, - row - 1
            )
            if second_half[idx] == '#':
                folded_paper[position_to_update] = '#'
    
    return folded_paper


def fold_paper(paper: np.ndarray, fold_op: FoldOp) -> np.ndarray:
    if fold_op.direction == FoldDirection.X:
        return fold_left(paper, fold_op.pos)
    else:
        return fold_up(paper, fold_op.pos)


def count_hashes_after_fold(instructions: Input) -> int:
    folded = fold_paper(instructions.paper, instructions.fold_ops[0])
    return np.count_nonzero(folded == '#')


def extract_code(instructions: Input) -> str:
    folded = instructions.paper

    for op in instructions.fold_ops:
        folded = fold_paper(folded, op)
    
    result = '\n'.join([
        ''.join(map(str, folded[i])) for i in range(folded.shape[0])
        ])

    return result

if __name__ == '__main__':
    test_input = read_input('input_test.txt')
    instructions = read_input('input.txt')

    assert count_hashes_after_fold(test_input) == 17
    assert count_hashes_after_fold(instructions) == 675

    print(extract_code(instructions))
