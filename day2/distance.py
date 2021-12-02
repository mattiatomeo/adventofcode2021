def hor_depth_product(measures):
    horizontal = 0
    depth = 0
    aim = 0

    for direction, dist in measures:
        if direction == "forward":
            horizontal += dist
            depth += aim * dist
        elif direction == "down":
            aim += dist
        else:  # "up"
            aim -= dist

    return horizontal * depth


def main():
    def split_row(row):
        direction, dist = row.split(" ")
        return direction, int(dist)

    with open("input.txt", "r") as fp:
        measures = [split_row(value) for value in fp.readlines()]

    print(hor_depth_product(measures))


if __name__ == '__main__':
    main()