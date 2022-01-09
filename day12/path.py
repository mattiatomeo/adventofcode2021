import dataclasses
import copy
from sys import path


from typing import List, Dict, Tuple, Set



@dataclasses.dataclass(frozen=True)
class Cave:
    name: str

    def is_small(self) -> bool:
        return self.name.islower()
    
    def is_big(self) -> bool:
        return self.name.isupper()

    def __str__(self) -> str:
        return f"{self.name}"


START_CAVE = Cave('start')
END_CAVE = Cave('end')


@dataclasses.dataclass
class SubterraneanNetwork:
    neighbors: Dict[Cave, List[Cave]] = dataclasses.field(default_factory=dict, init=False)
    
    def get_neighbors(self, cave: Cave) -> List[Cave]:
        return self.neighbors[cave]
    
    def add_cave(self, cave: Cave):
        if cave not in self.neighbors:
            self.neighbors[cave] = list()
    
    def add_connection(self, first: Cave, second: Cave):
        self.neighbors[first].append(second)
        self.neighbors[second].append(first)
    
    def __str__(self) -> str:
        return f"{self.neighbors}"

    @staticmethod
    def load_from_file(filepath: str) -> "SubterraneanNetwork":
        def extract_connection(file_row: str) -> Tuple[Cave, Cave]:
            first_cave_name, second_cave_name = file_row.split('-')

            return Cave(first_cave_name), Cave(second_cave_name)
        
        subterranean = SubterraneanNetwork()

        with open(filepath) as fp:
            for row in fp.readlines():
                first_cave, second_cave = extract_connection(row.strip())

                subterranean.add_cave(first_cave)
                subterranean.add_cave(second_cave)
                subterranean.add_connection(first_cave, second_cave)
        
        return subterranean
    

@dataclasses.dataclass
class SubterraneanPath:
    path: List[Cave] = dataclasses.field(default_factory=list, init=False)
    has_small_cave_traversed_twice: bool = dataclasses.field(default=False, init=False)
    traversed: Set[Cave] = dataclasses.field(default_factory=set, init=False)

    def can_move_to_cave(self, cave: Cave) -> bool:
        if cave.is_big() or cave not in self.traversed:
            return True

        if cave in self.traversed and not self.has_small_cave_traversed_twice:
            return True
        
        return False
   
    def move_to_cave(self, cave: Cave):
        if cave.is_small() and cave in self.traversed:
            self.has_small_cave_traversed_twice = True
            
        self.path.append(cave)
        self.traversed.add(cave)
    
    def get_last_traversed_cave(self) -> Cave:
        return self.path[-1]
    
    def path_ended(self) -> bool:
        return self.get_last_traversed_cave() == END_CAVE


def step_1(subterranean: SubterraneanNetwork) -> int:
    path_to_end = 0
    
    current_paths = [[START_CAVE]]

    while len(current_paths) > 0:
        path = current_paths.pop()

        for neighbor in subterranean.get_neighbors(path[-1]):
            if neighbor in path and not neighbor.is_big():
                continue

            if neighbor == END_CAVE:
                path_to_end += 1
            else:
                current_paths.append(path + [neighbor])


    return path_to_end


def step_2(subterranean: SubterraneanNetwork) -> int:
    path_to_end = 0
    
    def copy_path(path: SubterraneanPath) -> SubterraneanPath:
        return copy.deepcopy(path)
    
    first_path = SubterraneanPath()
    first_path.move_to_cave(START_CAVE)
    current_paths = [first_path]

    while len(current_paths) > 0:
        path = current_paths.pop()
        
        last_cave = path.get_last_traversed_cave()
        for neighbor in subterranean.get_neighbors(last_cave):
            if neighbor == START_CAVE:
                continue

            new_path = copy_path(path)
            if new_path.can_move_to_cave(neighbor):
                new_path.move_to_cave(neighbor)

                if not new_path.path_ended():
                    current_paths.append(new_path)
                else:
                    path_to_end += 1

    return path_to_end


def main():
    sub_example_1 = SubterraneanNetwork.load_from_file('input_test_1.txt')
    assert step_1(sub_example_1) == 10

    sub_example_2 = SubterraneanNetwork.load_from_file('input_test_2.txt')
    assert step_1(sub_example_2) == 19

    sub_example_3 = SubterraneanNetwork.load_from_file('input_test_3.txt')
    assert step_1(sub_example_3) == 226

    sub_network = SubterraneanNetwork.load_from_file('input_test_4.txt')
    assert step_1(sub_network) == 5457

    assert step_2(sub_example_1) == 36
    assert step_2(sub_example_2) == 103
    assert step_2(sub_network) == 128506


if __name__ == '__main__':
    main()
