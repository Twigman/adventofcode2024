from enum import Enum

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Coord(x={self.x}, y={self.y})"
    
    def __eq__(self, other):
        return isinstance(other, Coord) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))
    
    def copy(self):
        return Coord(self.x, self.y)


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Field(Enum):
    END = 1
    OBSTRUCTION = 2
    FREE = 3


def load_data_from_file(filename: str) -> list:
    with open(filename) as f:
        data = f.readlines()
    return data


def get_guard_pos(g_map: list) -> Coord:
    for counter in range(0, len(g_map)):
        try:
            index = g_map[counter].index('^')
            return Coord(index, counter)
        except ValueError:
            pass    
    return None


def check_next_field(g_map: list, target_field: Coord) -> Field:
    if target_field.x > (len(g_map[0]) - 1) or target_field.y > (len(g_map) - 1) or target_field.x < 0 or target_field.y < 0:
        return Field.END
    elif g_map[target_field.y][target_field.x] == '#':
        return Field.OBSTRUCTION
    else:
        return Field.FREE


def change_direction(direction: Direction) -> Direction:
    if direction == Direction.UP:
        return Direction.RIGHT
    elif direction == Direction.RIGHT:
        return Direction.DOWN
    elif direction == Direction.DOWN:
        return Direction.LEFT
    else:
        return Direction.UP


def do_step(g_map: list, pos: Coord, direction: Direction, visited_set: set) -> tuple[Coord, Direction, set]:
    target_field = Coord(0, 0)

    if direction == Direction.UP:
        target_field.x = pos.x
        target_field.y = pos.y - 1
    elif direction == Direction.DOWN:
        target_field.x = pos.x
        target_field.y = pos.y + 1
    elif direction == Direction.LEFT:
        target_field.x = pos.x - 1
        target_field.y = pos.y
    else:
        target_field.x = pos.x + 1
        target_field.y = pos.y

    next_field = check_next_field(g_map, target_field)

    if next_field == Field.OBSTRUCTION:
        direction = change_direction(direction)
        return do_step(g_map, pos, direction, visited_set)
    elif next_field == Field.FREE:
        pos = target_field
        visited_set.add(pos)

        return pos, direction, visited_set
    else:
        # end reached
        return None, None, visited_set


input_file = 'input.txt'
guard_map = []

guard_map = load_data_from_file(input_file)
guard_map = [line.strip() for line in guard_map]

curr_pos = get_guard_pos(guard_map)
start_pos = curr_pos.copy()
dist_visited_pos_set = set()
finished = False
moving_direction = Direction.UP
counter = 0


#print(guard_map)
print(f"x max: {len(guard_map[0]) - 1}")
print(f"y max: {len(guard_map) - 1}")
print(f"start at: {curr_pos}")

while not finished:
    curr_pos, moving_direction, dist_visited_pos_set = do_step(guard_map, curr_pos, moving_direction, dist_visited_pos_set)

    if curr_pos is None:
        finished = True

    counter += 1

print("Part 1:")
print(f"distinct visited positions: {len(dist_visited_pos_set)}")
