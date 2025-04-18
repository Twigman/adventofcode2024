input_file = "input.txt"

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Coord(x={self.x}, y={self.y})"

text = []
word = 'XMAS'

def load_data_from_file(filename: str) -> list:
    with open(filename) as f:
        data = f.readlines()
    return data


def count_forwards_in_line(line: str) -> int:
    return line.count(word)


def count_backwards_in_line(line: str) -> int:
    return line.count(word[::-1])


def is_xmas_at_coords(text: list, index_list: list) -> bool:
    letter_counter = 0

    if len(index_list) == len(word):
        for index_counter in range(0, len(index_list)):
            curr_pos = index_list[index_counter]
            if text[curr_pos.y][curr_pos.x] == word[index_counter]:
                letter_counter += 1
    return True if letter_counter == len(word) else False


def count_up(text: list, pos: Coord) -> int:
    if (pos.y - (len(word) - 1)) >= 0:
        # search
        index_list = []
        for k in range(0, len(word)):
            index_list.append(Coord(pos.x, pos.y - k))
        return 1 if is_xmas_at_coords(text, index_list) else 0
    else:
        return 0
    

def count_down(text: list, pos: Coord) -> int:
    if (pos.y + (len(word) - 1)) < len(text):
        # search
        index_list = []
        for k in range(0, len(word)):
            index_list.append(Coord(pos.x, pos.y + k))
        return 1 if is_xmas_at_coords(text, index_list) else 0
    else:
        return 0
    

def count_diagonal_up_right(text: list, pos: Coord) -> int:
    if (pos.y - (len(word) - 1)) >= 0 and (pos.x + (len(word) -1)) < len(text):
        # search
        index_list = []
        for k in range(0, len(word)):
            index_list.append(Coord(pos.x + k, pos.y - k))
        return 1 if is_xmas_at_coords(text, index_list) else 0
    else:
        return 0
    

def count_diagonal_up_left(text: list, pos: Coord) -> int:
    if (pos.y - (len(word) - 1)) >= 0 and (pos.x - (len(word) -1)) >= 0:
        # search
        index_list = []
        for k in range(0, len(word)):
            index_list.append(Coord(pos.x - k, pos.y - k))
        return 1 if is_xmas_at_coords(text, index_list) else 0
    else:
        return 0
    

def count_diagonal_down_left(text: list, pos: Coord) -> int:
    if (pos.y + (len(word) - 1)) < len(text) and (pos.x - (len(word) -1)) >= 0:
        # search
        index_list = []
        for k in range(0, len(word)):
            index_list.append(Coord(pos.x - k, pos.y + k))
        return 1 if is_xmas_at_coords(text, index_list) else 0
    else:
        return 0
    

def count_diagonal_down_right(text: list, pos: Coord) -> int:
    if (pos.y + (len(word) - 1)) < len(text) and (pos.x + (len(word) -1)) < len(text):
        # search
        index_list = []
        for k in range(0, len(word)):
            index_list.append(Coord(pos.x + k, pos.y + k))
        return 1 if is_xmas_at_coords(text, index_list) else 0
    else:
        return 0

text = load_data_from_file(input_file)

X_MAX = len(text[0]) - 1
Y_MAX = len(text)
xmas_counter = 0

for i in range(0, Y_MAX):
    xmas_counter += count_forwards_in_line(text[i])
    xmas_counter += count_backwards_in_line(text[i])

    for j in range(0, X_MAX):
        if text[i][j] == word[0]:
            xmas_counter += count_up(text, Coord(j, i))
            xmas_counter += count_down(text, Coord(j, i))
            xmas_counter += count_diagonal_up_right(text, Coord(j, i))
            xmas_counter += count_diagonal_up_left(text, Coord(j, i))
            xmas_counter += count_diagonal_down_left(text, Coord(j, i))
            xmas_counter += count_diagonal_down_right(text, Coord(j, i))

print(f"XMAS counter: {xmas_counter}")