import numpy as np
from itertools import combinations
from math import gcd

def load_data_from_file(filename: str) -> list:
    with open(filename) as f:
        data = f.readlines()
    return data


def map_to_num_matrix(r_map: list) -> tuple[np.array, dict]:
    # input to np array
    char_array = np.array([list(row.strip()) for row in r_map])
    # get all characters included in the array
    unique_chars = np.unique(char_array)
    # build a map and assign numbers to each character
    char_to_int_mapping = { char: i for i, char in enumerate(unique_chars) }
    # build a matrix and replace characters with the assigned numbers
    mapper = np.vectorize(lambda c: char_to_int_mapping[c])
    return mapper(char_array), char_to_int_mapping


def normalize_vec(vec: np.array) -> np.array:
    # greatest common divisor
    g = gcd(vec[0], vec[1])
    # whole number division if g exists
    return vec // g if g != 0 else vec


def walk_line(p: np.array, vec: np.array, shape: tuple) -> list:
    points = []
    # backward
    new_p = p.copy()
    on_map = True

    while on_map:
        new_p = new_p - vec

        if not (0 <= new_p[0] < shape[0] and 0 <= new_p[1] < shape[1]):
            on_map = False
        else:
            points.append(tuple(new_p))

    # include starting point
    points.append(tuple(p))

    # forwards
    new_p = p.copy()
    on_map = True

    while on_map:
        new_p = new_p + vec

        if not (0 <= new_p[0] < shape[0] and 0 <= new_p[1] < shape[1]):
            on_map = False
        else:
            points.append(tuple(new_p))
    return points


def calc_antinodes_for_frequency(m: np.array, frequency: int) -> np.array:
    # get all antennas using a specific frequency
    antenna_coords = np.argwhere(m == frequency)
    n = len(antenna_coords)

    if n < 2:
        # no or one antenna
        return None
    
    antinode_set = set()
    index = 0
    # iterate over every combination of coords
    for i, j in combinations(range(len(antenna_coords)), 2):
        # distance vector
        dist_vec = normalize_vec(antenna_coords[j] - antenna_coords[i])
        # get all point on crossing the vector
        points = walk_line(antenna_coords[i], dist_vec, m.shape)
        antinode_set.update(points)

    return np.array(list(antinode_set), dtype=int)


def filter_coords_outside_map(dim: tuple, coords: np.array) -> np.array:
    # only coords on the map
    valid_mask = (
        (coords[:, 0] >= 0) &
        (coords[:, 0] < dim[0]) &
        (coords[:, 1] >= 0) &
        (coords[:, 1] < dim[1])
    )
    return coords[valid_mask]

input_file = 'input.txt'
raw_map = load_data_from_file(input_file)
coord_list = []
m, char_mapping = map_to_num_matrix(raw_map)

for c in char_mapping:
    if c == '.':
        continue
    antinode_coords = calc_antinodes_for_frequency(m, char_mapping[c])
    coord_list.append(antinode_coords)

# collect unique coords
all_antinodes = np.vstack(coord_list)
antinodes_on_map = filter_coords_outside_map(m.shape, all_antinodes)
unique_antinodes_on_map = np.unique(antinodes_on_map, axis=0)

print('Part 2:')
print(f"antinodes on map: {len(unique_antinodes_on_map)}")