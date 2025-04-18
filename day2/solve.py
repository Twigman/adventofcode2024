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


def is_safe(record: np.array) -> bool:
    diffs = np.abs(np.diff(record))
    increasing = np.all(record[1:] > record[:-1])
    decreasing = np.all(record[1:] < record[:-1])
    return (increasing or decreasing) and np.all((diffs >= 1) & (diffs <= 3))


def try_fix_record(record: np.arange) -> np.array:
    for i in range(len(record)):
        candidate = np.delete(record, i)
        if is_safe(candidate):
            return candidate  # fixed
    return None  # not fixable


def apply_rules(records: list):
    counter = 0
    safe_r = []
    safe_i = []

    for record in records:
        if is_safe(record):
            safe_r.append(record)
            safe_i.append(counter)
        counter += 1
    return safe_r, safe_i

# check the following rules
# 1. all levels increasing or decreasing
# 2. levels differ by 1-3
safe_records = []
safe_indizes = []

safe_records, safe_indizes = apply_rules(unusual_records)

print("Part 1:")
print(f"#records passed rule 2: {len(safe_records)}")

######################################################
# Part 2
######################################################

records_to_check = unusual_records.copy()
# remove safe records
for i in sorted(safe_indizes, reverse=True):
    del records_to_check[i]

dampener_records = []
bad_preselection_counter = 0

for record in records_to_check:
    # at least use a little bit logic before bruteforce
    diffs = np.diff(record)
    # unsave levels are
    # 0 = redundant
    # +/- switch
    # values larger/smaller 3/-3
    
    # 0
    # redudant entry -> remove
    if 0 in diffs:
        # equal elements
        rm_i = np.where(diffs == 0)[0]

        if len(rm_i) >= 3:
            # to many
            bad_preselection_counter += 1
            continue
    # check signs
    sign_change = (diffs[:-1] * diffs[1:]) < 0

    if np.any(sign_change):
        # sign changes detected
        # level not increasing/decreasing
        sign_change_indices = np.where(sign_change)[0]

        if len(sign_change_indices) >= 3:
            # no chance to be a valid record
            bad_preselection_counter += 1
            continue
        elif len(sign_change_indices) == 2:
            # consecutive indices
            if sign_change_indices[0] == (sign_change_indices[1] - 1):
                # wrong level in between
                pass
            else:
                # no chance to be a valid record
                bad_preselection_counter += 1
                continue
        else:
            # one index
            pass
    
    # check values
    diffs = np.abs(np.diff(record))
    num_to_large = np.sum(diffs > 3)

    if num_to_large >= 2:
        bad_preselection_counter += 1
        continue
    else:
        pass

    # try and error
    fixed = try_fix_record(record)
    if fixed is not None:
        dampener_records.append(fixed)

print("Part 2:")
print(f"testing: {len(records_to_check)}")
print(f"excluded through preselection: {bad_preselection_counter}")
print(f"solution part 1: {len(safe_records)}")
print(f"additional: {len(dampener_records)}")
print(f"#records with tolerance: {len(dampener_records) + len(safe_records)}")