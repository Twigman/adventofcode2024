input_file = "input.txt"

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Coord(x={self.x}, y={self.y})"

text = []
word1 = 'MAS'
word2 = 'SAM'

def load_data_from_file(filename: str) -> list:
    with open(input_file) as f:
        data = f.readlines()
    return data


def is_word_at_coords(text: list, index_list: list, search_word: str) -> bool:
    letter_counter = 0

    if len(index_list) == len(search_word):
        for index_counter in range(0, len(index_list)):
            curr_pos = index_list[index_counter]
            if text[curr_pos.y][curr_pos.x] == search_word[index_counter]:
                letter_counter += 1
    return True if letter_counter == len(search_word) else False
    
    

def count_x_mas(text: list, pos: Coord) -> int:
    up_down_match = False
    down_up_match = False
    up_down_coords = []
    down_up_coords = []

    # down right
    if (pos.y + 1) < len(text) and (pos.x + 1) < len(text):
        # down left
        if (pos.y + 1) < len(text) and (pos.x - 1) >= 0:
            # up right
            if (pos.y - 1) >= 0 and (pos.x + 1) < len(text):
                # up left
                if (pos.y - 1) >= 0 and (pos.x - 1) >= 0:
                    # enough space
                    # generate coords
                    for k in range(0, len(word1)):
                        down_up_coords.append(Coord((pos.x - 1) + k, (pos.y + 1) - k))
                        up_down_coords.append(Coord((pos.x - 1) + k, (pos.y - 1) + k))
                    # mas down-up
                    if is_word_at_coords(text, down_up_coords, word1):
                        down_up_match = True
                    elif is_word_at_coords(text, down_up_coords, word2):
                        down_up_match = True
                    else:
                        return 0

                    # mas up-down
                    if is_word_at_coords(text, up_down_coords, word1):
                        up_down_match = True
                    elif is_word_at_coords(text, up_down_coords, word2):
                        up_down_match = True
                    else:
                        return 0
                    
                    if up_down_match and down_up_match:
                        return 1
    return 0
    

text = load_data_from_file(input_file)

X_MAX = len(text[0]) - 1
Y_MAX = len(text)
x_mas_counter = 0

for i in range(0, Y_MAX):
    for j in range(0, X_MAX):
        if text[i][j] == word1[1]:
            x_mas_counter += count_x_mas(text, Coord(j, i))

print(f"X-MAS counter: {x_mas_counter}")