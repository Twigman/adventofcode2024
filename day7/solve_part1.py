import re
import numpy as np

def load_data_from_file(filename: str) -> list:
    with open(filename) as f:
        data = f.readlines()
    return data


def extract_numbers_from(line: str) -> np.array:
    res = re.findall(r'\d+', line)
    return np.array(res, dtype=int)


def generate_solution_pattern(eq: np.array) -> np.array:
    allowed_ops = 2
    n_pos = (len(eq) - 2)
    if n_pos > 0:
        n_variations = allowed_ops ** n_pos
        ops = ((np.arange(n_variations)[:, None] >> np.arange(n_pos)[::-1]) & 1)
        return ops
    return None


def is_solvable(eq: np.array, ops: np.array) -> bool:
    for op_bits in ops:
        res = eq[1]
        for i, bit in enumerate(op_bits):
            if bit == 0:
                res += eq[2 + i]
            else:
                res *= eq[2 + i]
        if res == eq[0]:
            return True
    return False


input_file = 'input.txt'
eqs = load_data_from_file(input_file)
sum_solved_eq = 0

for line in eqs:
    eq = extract_numbers_from(line)
    ops = generate_solution_pattern(eq)

    if ops is None:
        continue

    if is_solvable(eq, ops):
        sum_solved_eq += eq[0]

print('Part 1:')
print(f"solution: {sum_solved_eq}")