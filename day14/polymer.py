import array
from collections import Counter
import functools
from tempfile import template
from typing import Dict, Tuple
from functools import partial


PolymerFormula = array.array
InsertionRule = Dict[Tuple[str, str], str]


init_formula = functools.partial(PolymerFormula, 'B')


def read_input(filepath: str) -> Tuple[PolymerFormula, InsertionRule]:
    def parse_rule(row):
        monomer_pair, monomer_to_insert = row.split(' -> ')
        return tuple(map(ord, monomer_pair)), ord(monomer_to_insert)
    
    with open(filepath, 'r') as fp:
        template = init_formula(map(ord, fp.readline().strip()))

        fp.readline()  # Skip empty row

        rules = {}
        while (row := fp.readline()) != '':
            pair, monomer = parse_rule(row.strip())

            rules[pair] = monomer

        return template, rules



def polymerization(template: PolymerFormula, rules: InsertionRule, step: int) -> PolymerFormula:
    result = template
    
    for _ in range(step):
        curr_formula = init_formula([result[0]])

        for pos in range(1, len(result)):
            monomer_pair = (result[pos - 1], result[pos])

            if monomer_pair in rules:
                curr_formula.append(rules[monomer_pair])
            
            curr_formula.append(monomer_pair[1])

        result = curr_formula
    
    return result


def print_formula(formula: PolymerFormula):
    print(''.join(map(chr, formula)))


def start_process(template: PolymerFormula, rules: InsertionRule, step: int) -> int:
    monomer_count = Counter([template[1]])

    @functools.lru_cache
    def sequence_pair(first: int, second: int) -> Dict[str, int]:
        current = init_formula([first, second])
        polymer = polymerization(current, rules, step)

        occurrences = Counter(polymer)
        occurrences[current[0]] -= 1

        return occurrences

    for pos in range(0, len(template) - 1):
        occurrences = sequence_pair(template[pos], template[pos + 1])

        monomer_count.update(occurrences)
    
    sorted_by_occurrence = monomer_count.most_common()

    most_occurrent = sorted_by_occurrence[0][1]
    least_occurrent = sorted_by_occurrence[-1][1]

    return most_occurrent - least_occurrent


def main():
    example = read_input('input_test.txt')
    
    polymer_input = read_input('input.txt')

    assert start_process(*example, 10) == 1588
    assert start_process(*polymer_input, 10) == 3213


if __name__ == '__main__':
    main()
