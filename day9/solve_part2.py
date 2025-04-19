import os

def load_data_from_file(filename: str) -> list:
    with open(filename) as f:
        data = f.readlines()
    return data


def expand_input(data: str) -> list:
    # e.g. input: '12345'
    # -> output: ['0', '.', '.', '1', '1', '1', '.', '.', '.', '.', '2', '2', '2', '2', '2']
    id = 0
    blocks = []
    is_file = True

    for digit in data:
        length = int(digit)
        if is_file:
            blocks.extend([str(id)] * length)
            id += 1
        else:
            blocks.extend([FREE_SPACE] * length)
        is_file = not is_file
    return blocks


def find_last_file_block(data: list, moved: dict) -> tuple[int, int]:
    index = len(data) - 1
    value = FREE_SPACE
    start_index = 0
    end_index = 0

    while index >= 0:
        if data[index] != FREE_SPACE and value == FREE_SPACE:
            if data[index] in moved:
                # already moved, skip file data
                new_index = moved[data[index]] - 1
                # problem with unmoved data in moved -> endless loop
                if new_index < index:
                    index = new_index
                else:
                    index -= 1
                continue
            # data block detected
            end_index = index
            value = data[index]
        elif value != FREE_SPACE and data[index] != value:
            # start of new block detected
            start_index = index + 1
            break
        else:
            # free space or still in file block
            index -= 1
            continue
        index -= 1
    return start_index, end_index


def find_gap_in_data(data: list, size: int, start_pos: int) -> int:
    start_index = 0
    free_block = 0

    # find gap for block
    for index in range(0, start_pos):
        if data[index] == FREE_SPACE:
            # free space
            free_block += 1

            if free_block == size:
                # big enough
                start_index = index - free_block + 1
                return start_index
            continue
        else:
            free_block = 0
    return -1


def pack_data(data: list) -> list:
    moved = {}
    while True:
        lb_start, lb_end = find_last_file_block(data, moved)

        if lb_start == 0 and lb_end == 0:
            return data

        block_size = lb_end - lb_start + 1

        gap_start = find_gap_in_data(data, block_size, lb_start)

        if gap_start != -1:
            # move file block
            for index in range(0, block_size):
                data[gap_start + index] = data[lb_start + index]
                data[lb_start + index] = FREE_SPACE
            moved[data[gap_start]] = lb_start
        else:
            moved[data[lb_start]] = lb_start


def calc_checksum(data: list) -> int:
    checksum = 0

    for i, value in enumerate(data):
        if value == FREE_SPACE:
            continue
        checksum += int(value) * i
    
    return checksum


input_file = 'input.txt'
script_dir = os.path.dirname(__file__)
input_path = os.path.join(script_dir, input_file)
FREE_SPACE = '.'
raw_data = load_data_from_file(input_path)
blocks = expand_input(raw_data[0])
packed_data = pack_data(blocks)
checksum = calc_checksum(packed_data)

print('Part 2:')
print(f"checksum: {checksum}")