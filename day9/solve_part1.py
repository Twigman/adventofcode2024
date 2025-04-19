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


def pack_data(data: list) -> list:
    length = len(data)
    read = length - 1

    for write in range(0, length):
        if data[write] == FREE_SPACE:
            # search next id
            while data[read] == FREE_SPACE:
                read -= 1

            # packing complete?
            if read < write:
                break

            data[write] = data[read]
            data[read] = FREE_SPACE
            read -= 1
    return data
    

def calc_checksum(data: list) -> int:
    checksum = 0

    for i, value in enumerate(data):
        if value == FREE_SPACE:
            break
        checksum += int(value) * i
    
    return checksum


FREE_SPACE = '.'
input_file = 'input.txt'
raw_data = load_data_from_file(input_file)
blocks = expand_input(raw_data[0])
packed_data = pack_data(blocks)
checksum = calc_checksum(packed_data)

#print(packed_data)
print('Part 1:')
print(f"checksum: {checksum}")