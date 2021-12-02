def count_increase(measures):
    return sum(int(measures[i] < measures[i + 1]) for i in range(len(measures) - 1))


def count_window_increase(measures):
    return sum(int(measures[i + 3] > measures[i]) for i in range(len(measures) - 3))


def main():
    with open("input.txt", "r") as fp:
        measures = [int(value) for value in fp.readlines()]

    print(count_window_increase(measures))


if __name__ == '__main__':
    main()