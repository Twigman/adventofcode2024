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


def get_next_pos(pos: Coord, direction: Direction) -> Coord:
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
    return target_field


def do_step(g_map: list, pos: Coord, direction: Direction, visited_set: set) -> tuple[Coord, Direction, set]:
    target_field = get_next_pos(pos, direction)
    next_field = check_next_field(g_map, target_field)

    if is_loop_detected(all_visited_fields):
        return Coord(-1, -1), None, visited_set

    if next_field == Field.OBSTRUCTION:
        direction = change_direction(direction)
        return pos, direction, visited_set
        #return do_step(g_map, pos, direction, visited_set)
    elif next_field == Field.FREE:
        pos = target_field
        visited_set.add(pos)
        all_visited_fields.append(pos)

        return pos, direction, visited_set
    else:
        # end reached
        return None, None, visited_set
    

def is_loop_detected(all_visited: list) -> bool:
    # last two postions
    if len(all_visited) > 2:
        sequence = all_visited[-2:]
        search_space = all_visited[:-2]
        return any(search_space[i:i+len(sequence)] == sequence for i in range(len(search_space) - len(sequence) + 1))
    else:
        return False
    

def place_obstruction(
        g_map: list,
        obstr_pos: Coord,
        start_pos: Coord,
        obstr_counter: int,
        placed_set: set
    ) -> tuple[list, int, bool, set]:
    in_bounds = (
        0 <= obstr_pos.x < len(g_map[0]) and
        0 <= obstr_pos.y < len(g_map)
    )
    if obstr_pos != start_pos and in_bounds:
        if g_map[obstr_pos.y][obstr_pos.x] != '#':
            # already placed at pos
            if not obstr_pos in placed_set:
                row = list(g_map[obstr_pos.y])  
                row[obstr_pos.x] = '#'
                g_map[obstr_pos.y] = ''.join(row)
                obstr_counter += 1
                placed_set.add(obstr_pos)
                return g_map, obstr_counter, True, placed_set
            else:
                return g_map, obstr_counter, True, placed_set
        else:
            return g_map, obstr_counter, False, placed_set
    else:
        return g_map, obstr_counter, False, placed_set

#############################################
# Part 2
#############################################

# count obstacle positions where the guard would get stuck in a loop

input_file = 'input.txt'

original_map = load_data_from_file(input_file)
original_map = [line.strip() for line in original_map]

MAX_OBSTR_PLACEMENTS = 10000
placed_obstructions = 0
MAX_STEPS = 20000
MAX_RUNS = 10000
MAX_OBSTR_TRYS = 50
last_placed_obstruction_at_steps = 0
produced_loops = 0
run_counter = 1
obstr_placement_trys = 0
start_pos = get_guard_pos(original_map)
placed_obstructions_set = set()

print(f"max obstuction placements: {MAX_OBSTR_PLACEMENTS}")
print(f"start pos: {start_pos}")

while placed_obstructions < MAX_OBSTR_PLACEMENTS and run_counter < MAX_RUNS and obstr_placement_trys < MAX_OBSTR_TRYS:
    guard_map = original_map.copy()
    curr_pos = start_pos.copy()
    dist_visited_pos_set = set()
    finished = False
    moving_direction = Direction.UP
    counter = 0
    finished = False
    all_visited_fields = []
    obstr_placed = False
    
    print(f"starting run: {run_counter}")

    while not finished:
        # try to place obstruction
        if not obstr_placed and counter > last_placed_obstruction_at_steps:
            next_pos = get_next_pos(curr_pos, moving_direction)
            guard_map, placed_obstructions, obstr_placed, placed_obstructions_set = place_obstruction(guard_map, next_pos, start_pos, placed_obstructions, placed_obstructions_set)
            obstr_placement_trys += 1

            if obstr_placed:
                print(f"placed at {next_pos}!")
                last_placed_obstruction_at_steps = counter
                obstr_placement_trys = 0
            else:
                print(f"{next_pos} not working")

        curr_pos, moving_direction, dist_visited_pos_set = do_step(guard_map, curr_pos, moving_direction, dist_visited_pos_set)

        if curr_pos is None:
            finished = True
            print(f"run {run_counter}: finished after {counter} steps at {all_visited_fields[-1]}")
        elif curr_pos.x == -1 and curr_pos.y == -1:
            print(f"loop detected after {counter} steps")
            produced_loops += 1
            break

        if counter == MAX_STEPS:
            print('!!! max steps reached !!!')
            break
        counter += 1
    run_counter += 1

if run_counter >= MAX_RUNS - 1:
    print("!!! max runs reached !!!")

if obstr_placement_trys >= MAX_OBSTR_TRYS -1:
    print("!!! max obstr_placement_trys reached !!!")

print("Part 2:")
print(f"placed obstructions: {placed_obstructions}")

print(f"produced loops: {produced_loops}")