import re

input_file = "input.txt"

instruction_string_list = []
sum_prod_part1 = 0

def load_data_from_file(filename: str) -> list:
    data = []
    # read instructions
    with open(input_file) as f:
        for line in f:
            data.append(line)
    return data


def execute_mul(instr: str) -> int:
    factors = re.findall(r'\d+', instr)
    if len(factors) == 2:
        return int(factors[0]) * int(factors[1])
    else:
        return 0

instruction_string_list = load_data_from_file(input_file)

for instruction_string in instruction_string_list:
    matches = re.findall(r'mul\(\d+,\d+\)', instruction_string)

    for match in matches:
        sum_prod_part1 += execute_mul(match)

print("Part 1:")
print(f"sum of products: {sum_prod_part1}")

sum_prod_part2 = 0
execute = True

# part 2
for instruction_string in instruction_string_list:
    index_do = 0
    index_dont = 0
    index_mul = 0
    
    # find do and dont
    do_pos = [m.start() for m in re.finditer(r'do\(\)', instruction_string)]
    dont_pos = [m.start() for m in re.finditer(r"don't\(\)", instruction_string)]
    mul_matches = [(m.group(), m.start()) for m in re.finditer(r"mul\(\d+,\d+\)", instruction_string)]

    for cursor in range(0, len(instruction_string)):
        if cursor == do_pos[index_do]:
            execute = True
            if index_do < len(do_pos) -1:
                index_do += 1
        elif cursor == dont_pos[index_dont]:
            execute = False
            if index_dont < len(dont_pos) -1:
                index_dont += 1
        else:
            pass

        if cursor == mul_matches[index_mul][1]:
            if execute:
                sum_prod_part2 += execute_mul(mul_matches[index_mul][0])
            else:
                pass

            if index_mul < len(mul_matches) -1:
                index_mul += 1

print("Part 2:")
print(f"sum of products: {sum_prod_part2}")