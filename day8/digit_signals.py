from typing import List, Set, Tuple, Union, Dict
from collections import Counter

SignalPattern = Set[str]
PrintedSegments = Set[str]

ProblemInputRow = Tuple[List[SignalPattern], List[PrintedSegments]]


def read_patterns_and_segments(file_path: str) -> List[ProblemInputRow]:
    def parse_sequence(seq: str) -> Union[List[SignalPattern], List[PrintedSegments]]:
        return list(map(set, seq.split()))

    def parse_display_patterns_and_seq(display_data: str) -> ProblemInputRow:
        return tuple(map(parse_sequence, display_data.split('|')))  # noqa

    with open(file_path, 'r') as f:
        return list(map(parse_display_patterns_and_seq, f.readlines()))


class SignalDecoder:
    def __init__(self, patterns: List[SignalPattern]):
        self.number_to_pattern = dict()  # type: Dict[int, SignalPattern]
        self._decode_patterns(patterns)

    def _decode_patterns(self, patterns: List[SignalPattern]):
        signals_map = {}  # type: Dict[str, str]
        unique_digits_pattern, skipped = self._find_unique_digits(patterns)

        signals_map['a'] = (unique_digits_pattern[7] - unique_digits_pattern[1]).pop()

        nine_pattern = next(
            pattern for pattern in skipped if len(pattern) == 6 and unique_digits_pattern[4] <= pattern
        )

        signals_map['g'] = (nine_pattern - unique_digits_pattern[4] - {signals_map['a']}).pop()

        signals_map['e'] = (unique_digits_pattern[8] - nine_pattern - set(signals_map.values())).pop()

        curr_identified_pattern = set(signals_map.values())
        two_pattern = next(
            pattern for pattern in skipped if len(pattern) == 5 and curr_identified_pattern <= pattern
        )

        signals_map['c'] = ((two_pattern - curr_identified_pattern) & unique_digits_pattern[1]).pop()
        signals_map['f'] = (unique_digits_pattern[1] - {signals_map['c']}).pop()

        query_for_d = set(signals_map.values()) - {signals_map['e']}
        three_pattern = next(
            pattern for pattern in skipped if len(pattern) == 5 and query_for_d <= pattern
        )

        signals_map['d'] = (three_pattern - query_for_d).pop()

        signals_map['b'] = (unique_digits_pattern[8] - set(signals_map.values())).pop()

        self._build_digit_patterns(signals_map)

    def _build_digit_patterns(self, signals_map: Dict[str, str]):
        self.number_to_pattern[0] = {
            signals_map['a'],
            signals_map['b'],
            signals_map['e'],
            signals_map['g'],
            signals_map['f'],
            signals_map['c'],
        }
        self.number_to_pattern[1] = {
            signals_map['c'],
            signals_map['f'],
        }
        self.number_to_pattern[2] = {
            signals_map['a'],
            signals_map['c'],
            signals_map['d'],
            signals_map['e'],
            signals_map['g'],
        }
        self.number_to_pattern[3] = {
            signals_map['a'],
            signals_map['c'],
            signals_map['d'],
            signals_map['f'],
            signals_map['g'],
        }
        self.number_to_pattern[4] = {
            signals_map['b'],
            signals_map['c'],
            signals_map['d'],
            signals_map['f'],
        }
        self.number_to_pattern[5] = {
            signals_map['a'],
            signals_map['b'],
            signals_map['d'],
            signals_map['f'],
            signals_map['g'],
        }
        self.number_to_pattern[6] = {
            signals_map['a'],
            signals_map['b'],
            signals_map['d'],
            signals_map['e'],
            signals_map['f'],
            signals_map['g'],
        }
        self.number_to_pattern[7] = {
            signals_map['a'],
            signals_map['c'],
            signals_map['f'],
        }
        self.number_to_pattern[8] = set(signals_map.values())
        self.number_to_pattern[9] = {
            signals_map['a'],
            signals_map['b'],
            signals_map['c'],
            signals_map['d'],
            signals_map['f'],
            signals_map['g'],
        }

    @staticmethod
    def _find_unique_digits(patterns: List[SignalPattern]) -> Tuple[Dict[int, SignalPattern], List[SignalPattern]]:
        skipped_patterns = []
        unique_digits_pattern = {}
        for pattern in patterns:
            match len(pattern):
                case 2:
                    unique_digits_pattern[1] = pattern
                case 3:
                    unique_digits_pattern[7] = pattern
                case 4:
                    unique_digits_pattern[4] = pattern
                case 7:
                    unique_digits_pattern[8] = pattern
                case _:
                    skipped_patterns.append(pattern)

        return unique_digits_pattern, skipped_patterns

    def translate_printed_segments(self, segments: List[PrintedSegments]) -> str:
        def translate_single_segment(segment: PrintedSegments) -> str:
            for number, pattern in self.number_to_pattern.items():
                if pattern == segment:
                    return str(number)

            RuntimeError(f'Cannot translate the pattern {segment}')

        return ''.join(map(translate_single_segment, segments))  # noqa


def intersection_size(s1: Set[str], s2: Set[str]) -> int:
    return len(s1 & s2)


def step_1(input_displays: List[ProblemInputRow]) -> int:
    unique_digits_count = 0
    unique_digits = set("1478")

    def count_occurences(decoded_disp: str) -> int:
        digit_count = Counter(decoded_disp)
        return sum(digit_count[digit] for digit in unique_digits)

    for display_pattern, printed_segments in input_displays:
        decoded_display = SignalDecoder(display_pattern).translate_printed_segments(printed_segments)
        unique_digits_count += count_occurences(decoded_display)

    return unique_digits_count


def step_2(input_displays: List[ProblemInputRow]) -> int:
    def parse_input_to_int(input_display: ProblemInputRow) -> int:
        display_pattern, printed_segments = input_display
        decoded_display = SignalDecoder(display_pattern).translate_printed_segments(printed_segments)

        return int(decoded_display)

    return sum(parse_input_to_int(row) for row in input_displays)


if __name__ == '__main__':
    test_input = read_patterns_and_segments('input_test.txt')
    real_input = read_patterns_and_segments('input.txt')

    assert step_1(test_input) == 26
    assert step_1(real_input) == 456

    assert step_2(real_input) == 1091609




