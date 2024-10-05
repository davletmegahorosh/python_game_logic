import random
def get_field_around_player(player_symbol, radius, map):
    for i, row in enumerate(map):
        for j, element in enumerate(row):
            if element == player_symbol:
                player_position = (i, j)
                break

    field_around_player = []
    for i in range(max(0, player_position[0] - radius), min(len(map), player_position[0] + radius + 1)):
        row = []
        for j in range(max(0, player_position[1] - radius), min(len(map[0]), player_position[1] + radius + 1)):
            row.append(map[i][j])
        field_around_player.append(row)

    return field_around_player


def move(direction_1, direction_2, data):
    data["player_moves"] += 1
    for j in [1,2]:
        player_position = [(i, row.index(j+2)) for i, row in enumerate(data["map"]) if j+2 in row][0]

        direction = direction_1 if j == 1 else direction_2
        print(player_position, direction)
        new_position = None

        if direction == 'left':
            new_position = (player_position[0], player_position[1] - 1)
        elif direction == 'right':
            new_position = (player_position[0], player_position[1] + 1)
        elif direction == 'top':
            new_position = (player_position[0] - 1, player_position[1])
        elif direction == 'bottom':
            new_position = (player_position[0] + 1, player_position[1])
        if 0 <= new_position[0] < 15 and 0 <= new_position[1] < 15:
            if data["map"][new_position[0]][new_position[1]] != 1:
                new = data['map'][new_position[0]][new_position[1]]
                prev = data["map"][player_position[0]][player_position[1]]
                if new == 2:
                    data["amount_food"] -= 1
                    data[f"fruits_{j}"] += 1
                elif new == 5:
                    data[f'is_alive_{j}'] = False
                    data['reason'] = "bomb"
                elif new == 3 or new == 4:
                    enemy = 2 if j == 1 else 1
                    data[f'is_slive_{enemy}'] = False
                    data['reason'] = "step"
                data["map"][player_position[0]][player_position[1]] = 0
                data["map"][new_position[0]][new_position[1]] = j + 2
    return data


def validate_python_syntax(file_path):
    try:
        with open(file_path, 'r') as file:
            code = file.read()
        compile(code, file_path, 'exec')
        return None
    except SyntaxError as e:
        return f"Syntax error in file: {str(e)}"


def validate_map_objects(map_data):
    count_fruits = 0
    for row in map_data:
        for cell in row:
            if cell not in [0, 1, 2, 3, 4, 5]:
                return f"Invalid object '{cell}' found on map. Allowed objects are 0, 1, 2, 3."
            if cell == 2:
                count_fruits += 1
    return count_fruits


def validate_player_function(context, player):
    if 'movePlayer' not in context:
        print(context)
        return f"Function 'movePlayer' is not found in the code. {player}"
    elif not callable(context['movePlayer']):
        return f"'movePlayer' is not a function.{player}"
    return None


def validate_player_surrounded(map_data):

    player_position = [(i, row.index(2)) for i, row in enumerate(map_data) if 2 in row][0]
    x, y = player_position

    surroundings = [
        map_data[x - 1][y] if x - 1 >= 0 else 0,
        map_data[x + 1][y] if x + 1 < len(map_data) else 0,
        map_data[x][y - 1] if y - 1 >= 0 else 0,
        map_data[x][y + 1] if y + 1 < len(map_data[0]) else 0
    ]

    if all(sur == 0 for sur in surroundings):
        return "Player is surrounded by walls and cannot move."
    return None


def validate_fruits_accessibility(map_data):
    from collections import deque

    player_position = [(i, row.index(2)) for i, row in enumerate(map_data) if 2 in row][0]
    fruits_positions = [(i, j) for i, row in enumerate(map_data) for j, cell in enumerate(row) if cell == 3]

    if not fruits_positions:
        return None

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visited = set()
    queue = deque([player_position])
    visited.add(player_position)

    while queue:
        x, y = queue.popleft()

        if (x, y) in fruits_positions:
            fruits_positions.remove((x, y))
            if not fruits_positions:
                return None

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(map_data) and 0 <= ny < len(map_data[0]) and (nx, ny) not in visited:
                if map_data[nx][ny] != 0:
                    queue.append((nx, ny))
                    visited.add((nx, ny))

    return "Some fruits are unreachable on the map."


def validate_move_direction(direction):
    if direction not in ['left', 'right', 'top', 'bottom']:
        return f"Invalid move direction '{direction}' returned. Allowed directions are: left, right, top, bottom."
    return None

