raw_updates = []
raw_rules = []
rules = []
update_file = 'input.txt'
rule_file = 'rules.txt'

def load_data_from_file(filename: str) -> list:
    with open(filename) as f:
        data = f.readlines()
    return data


def has_rule(a: int, b: int) -> bool:
    if [a, b] in rules:
        return True
    else:
        return False
    

def is_page_correct(pages: list, index: int) -> bool:
    correct_counter = 0
    for counter in range(index, len(pages)):
        if counter == 0:
            continue
        
        if has_rule(pages[index], pages[counter]):
            correct_counter += 1
    return True if correct_counter == (len(pages[index:]) -1) else False


def swap_pages(pages: list, source_index: int, taget_index: int) -> list :
    temp = pages[taget_index]
    pages[taget_index] = pages[source_index]
    pages[source_index] = temp
    return pages


def fix_page_order(pages: list, index: int) -> list:
    for counter in range(index, len(pages)):
        if counter == index:
            continue
        
        if has_rule(pages[index], pages[counter]):
            continue
        else:
            # fix
            # swap bad page with page behind it
            pages = swap_pages(pages, index, index + 1)
            pages = fix_page_order(pages, index + 1)
    return pages


def calc_score(data: list) -> int:
    score = 0
    for d in data:
        score += d[int(len(d) / 2)]
    return score


raw_updates = load_data_from_file(update_file)
raw_rules = load_data_from_file(rule_file)
correct_updates = []
incorrect_updates = []
score_part1 = 0

for rule in raw_rules:
    rules.append(list(map(int, rule.strip().split('|'))))

for update in raw_updates:
    correct_pages_counter = 0
    pages = list(map(int, update.strip().split(',')))
    
    # check page rules
    for index in range(0, len(pages)):
        if is_page_correct(pages, index):
            correct_pages_counter += 1
        else:
            # bad update
            continue
    if correct_pages_counter == len(pages):
        correct_updates.append(pages)
    else:
        print(f"only {correct_pages_counter} correct from {len(pages)}: {pages}")
        incorrect_updates.append(pages)

score_part1 = calc_score(correct_updates)

print('Part 1:')
print(f"score: {score_part1}")

######################################################
# Part 2: fix incorrect updates
######################################################

score_part2 = 0
corrected_updates = []

for incorrect_pages in incorrect_updates:
    corrected_counter = 0

    # check page rules
    for index in range(0, len(incorrect_pages)):
        corrected_pages = fix_page_order(incorrect_pages, index)

        if is_page_correct(corrected_pages, index):
            corrected_counter += 1
            continue
        else:
            # correct as long as it takes
            while not is_page_correct(corrected_pages, index):
                corrected_pages = fix_page_order(corrected_pages, index)
                print("additional corretion run")

            if is_page_correct(corrected_pages, index):
                corrected_counter += 1
                continue
            else:
                print(f"incorrect index: {index} in {corrected_pages}")
                continue

    if corrected_counter == len(corrected_pages):
        corrected_updates.append(corrected_pages)
    else:
        print(f"only {corrected_counter} correct from {len(corrected_pages)}: {corrected_pages}")


score_part2 = calc_score(corrected_updates)

print('Part 2:')
print(f"corrected {len(corrected_updates)} from {len(incorrect_updates)}")
print(f"score: {score_part2}")