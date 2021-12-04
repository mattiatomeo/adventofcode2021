import numpy as np


def read_diagnosis_records():
    with open("input.txt", "r") as f:
        return f.readlines()


def count_bit_at_pos(record: str, bit: str):
    return np.fromiter((int(digit == bit) for digit in record.strip()), dtype=np.int64)


def produce_entry_on_bit(diagnosis_records: list, bit: str) -> int:
    bit_set_count = np.sum(
        np.array(list(map(lambda record: count_bit_at_pos(record, bit), diagnosis_records))),
        axis=0
    )
    power_of_two = np.array([2 ** pos for pos in reversed(range(bit_set_count.shape[0]))])

    most_common_pos = np.where(
        bit_set_count > len(diagnosis_records) / 2, 1, 0
    )

    return np.sum(most_common_pos * power_of_two)


def step_1(diagnosis_records: list) -> int:
    return produce_entry_on_bit(diagnosis_records, "1") * produce_entry_on_bit(diagnosis_records, "0")


if __name__ == '__main__':
    records = read_diagnosis_records()
    print(step_1(records))

