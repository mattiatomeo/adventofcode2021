from collections import defaultdict
from typing import Dict, Tuple

PolymerFormula = Tuple
InsertionRule = Dict[Tuple[str, str], str]


def read_input(filepath: str) -> Tuple[PolymerFormula, InsertionRule]:
    def parse_rule(row):
        monomer_pair, monomer_to_insert = row.split(' -> ')
        return tuple(monomer_pair), monomer_to_insert
    
    with open(filepath, 'r') as fp:
        template = list(fp.readline().strip())

        fp.readline()  # Skip empty row

        rules = {}
        while (row := fp.readline()) != '':
            pair, monomer = parse_rule(row.strip())

            rules[pair] = monomer

        return template, rules


def polymerization(template: PolymerFormula, rules: InsertionRule, step: int) -> int:
    pairs = defaultdict(int)

    for couple in zip(template, template[1:]):
        pairs[couple] += 1
    
    def execute_next_step(last_step_result):
        step_result = defaultdict(int)
        for pair, count in last_step_result.items():
            try:
                monomer = rules[pair]
                step_result[pair[0], monomer] += count 
                step_result[monomer, pair[1]] += count
            except KeyError:
                step_result[pair] = count
        
        return step_result

    for _ in range(step):
        pairs = execute_next_step(pairs)
    
    ch_counter = defaultdict(int)

    for (first_monomer, _), count in pairs.items():
        ch_counter[first_monomer] += count
    
    ch_counter[template[-1]] += 1

    max_occurrence = max(ch_counter.values())
    min_occurrence = min(ch_counter.values())

    return max_occurrence - min_occurrence

def main():
    example = read_input('input_test.txt')
    
    polymer_input = read_input('input.txt')

    assert polymerization(*example, 10) == 1588
    assert polymerization(*polymer_input, 10) == 3213
    
    assert polymerization(*example, 40) == 2188189693529
    assert polymerization(*polymer_input, 40) == 3711743744429


if __name__ == '__main__': 
    main()
