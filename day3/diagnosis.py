import numpy as np


def read_diagnosis_records():
    with open("input.txt", "r") as f:
        return [row.strip() for row in f.readlines()]


def binary_to_int(binary_repr: np.array) -> int:
    power_of_two = np.array([2 ** pos for pos in reversed(range(binary_repr.shape[0]))])

    return np.sum(binary_repr * power_of_two)


def step_1(diagnosis_records: list) -> int:
    def calculate_rate(records: list, bit: str) -> int:
        def count_bit_at_pos(record: str, bit_to_count: str):
            return np.fromiter((int(digit == bit_to_count) for digit in record), dtype=np.int64)

        bit_set_count = np.sum(
            np.array(list(map(lambda record: count_bit_at_pos(record, bit), records))),
            axis=0
        )
        power_of_two = np.array([2 ** pos for pos in reversed(range(bit_set_count.shape[0]))])

        most_common_pos = np.where(
            bit_set_count > len(records) / 2, 1, 0
        )

        return np.sum(most_common_pos * power_of_two)

    return calculate_rate(diagnosis_records, "1") * calculate_rate(diagnosis_records, "0")


def step_2(diagnosis_records: list) -> int:
    def calculate_rating(records: np.array, filter_on_most_common: bool) -> int:
        rating = np.array(records)
        num_of_bits = records.shape[1]
        for pos in range(num_of_bits):
            remaining = rating.shape[0]
            if rating[:, pos].sum() >= remaining / 2:
                bit_filter = 0 + int(filter_on_most_common)
            else:
                bit_filter = 1 - int(filter_on_most_common)

            query = np.where(
                rating[:, pos] == bit_filter
            )
            rating = rating[query]

            if rating.shape[0] == 1:
                return binary_to_int(rating[0])

        raise RuntimeError("I shouldn't be here")

    binary_records = np.array([
        np.fromiter(map(int, list(record)), dtype=np.int64)
        for record in diagnosis_records
    ])

    oxygen_generator_rating = calculate_rating(binary_records, True)
    co2_scrubber_rating = calculate_rating(binary_records, False)
    return oxygen_generator_rating * co2_scrubber_rating


if __name__ == '__main__':
    diagnosis = read_diagnosis_records()
    print(step_1(diagnosis))
    print(step_2(diagnosis))

