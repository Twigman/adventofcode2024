import numpy as np

input_file = "input.txt"
num_records = 0

unusual_records = []

# read unusual data
with open(input_file) as f:
    for line in f:
        nums = list(map(int, line.strip().split()))
        unusual_records.append(np.array(nums))
        num_records += 1

# check the following rules
# 1. all levels increasing or decreasing
# 2. levels differ by 1-3
safe_records = []
num_passed_rule_one = 0


for record in unusual_records:
    is_increasing = np.all(record[1:] > record[:-1])
    is_decreasing = False

    if is_increasing:
        pass
    else:
        is_decreasing = np.all(record[1:] < record[:-1])

    if is_increasing or is_decreasing:
        num_passed_rule_one += 1
        diff = np.abs(np.diff(record))
        adjacent_check = np.all((diff >= 1) & (diff <= 3))

        if adjacent_check:
            safe_records.append(diff)

print(f"#records passed rule 1: {num_passed_rule_one}")
print(f"#records passed rule 2: {len(safe_records)}")