import math
from typing import List

Record = List[str]

SYNTAX_ERROR_SCORE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

AUTOCOMPLETITION_SCORE = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

OPEN_PARENTHESIS = {'(', '[', '{', '<'}

MATCHING_PARENTHESIS = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}


def read_input(file_path: str) -> List[Record]:
    with open(file_path, 'r') as f:
        return list(map(list, (row.strip() for row in f.readlines())))


def is_open_parenthesis(ch: str) -> bool:
    assert len(ch) == 1

    return ch in OPEN_PARENTHESIS


def are_parenthesis_matching(first: str, second: str) -> bool:
    return MATCHING_PARENTHESIS[first] == second


def get_record_error_score(record: Record) -> int:
    open_parenthesis = []
    pos = 0
    while pos < len(record):
        ch = record[pos]
        if is_open_parenthesis(ch):
            open_parenthesis.append(ch)
        else:
            last_open = open_parenthesis.pop()
            if not are_parenthesis_matching(last_open, ch):
                return SYNTAX_ERROR_SCORE[ch]

        pos += 1

    return 0


def get_syntax_error_score(records: List[Record]) -> int:
    return sum(map(get_record_error_score, records))


def get_autocompletition_score(records: List[Record]) -> int:
    def has_not_syntax_error(record: Record) -> bool:
        return get_record_error_score(record) == 0

    def get_autocomplete_score(record: Record) -> int:
        score = 0

        open_parenthesis = []
        for parenthesis in record:
            if is_open_parenthesis(parenthesis):
                open_parenthesis.append(parenthesis)
            else:
                open_parenthesis.pop()

        while len(open_parenthesis) > 0:
            open_ch = open_parenthesis.pop()
            closing_ch = MATCHING_PARENTHESIS[open_ch]
            score = score * 5 + AUTOCOMPLETITION_SCORE[closing_ch]

        return score

    autocomplete_scores = sorted(
        list(map(get_autocomplete_score, filter(has_not_syntax_error, records)))
    )

    winner_pos = len(autocomplete_scores) // 2
    return autocomplete_scores[winner_pos]


def main():
    navigation_records = read_input('input.txt')
    example_records = read_input('input_test.txt')

    assert get_syntax_error_score(example_records) == 26397
    assert get_syntax_error_score(navigation_records) == 243939
    assert get_autocompletition_score(example_records) == 288957
    assert get_autocompletition_score(navigation_records) == 2421222841


if __name__ == '__main__':
    main()
