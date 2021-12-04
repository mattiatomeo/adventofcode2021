def depth_increase_1(measures):
    return sum(int(measures[i] < measures[i + 1]) for i in range(len(measures) - 1))


def depth_increase_2(measures):
    return sum(int(measures[i + 3] > measures[i]) for i in range(len(measures) - 3))


def main():
    with open("input.txt", "r") as fp:
        measures = [int(value) for value in fp.readlines()]

    assert depth_increase_1(measures) == 1475
    assert depth_increase_2(measures) == 1516


if __name__ == '__main__':
    main()
