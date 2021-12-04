def find_position_1(movements):
    horizontal = 0
    depth = 0

    for direction, amount in movements:
        if direction == "forward":
            horizontal += amount
        elif direction == "down":
            depth += amount
        else:  # "up"
            depth -= amount

    return horizontal * depth


def find_position_2(movements):
    horizontal = 0
    depth = 0
    aim = 0

    for direction, amount in movements:
        if direction == "forward":
            horizontal += amount
            depth += aim * amount
        elif direction == "down":
            aim += amount
        else:  # "up"
            aim -= amount

    return horizontal * depth


def main():
    def split_row(row):
        direction, amount = row.split(" ")
        return direction, int(amount)

    with open("input.txt", "r") as fp:
        movements = [split_row(value) for value in fp.readlines()]

    assert find_position_1(movements) == 2322630
    assert find_position_2(movements) == 2105273490


if __name__ == '__main__':
    main()
