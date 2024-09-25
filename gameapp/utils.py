import os
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


def move(direction, data):
    data["player_moves"] += 1
    player_position = [(i, row.index(2)) for i, row in enumerate(data["map"]) if 2 in row][0]

    new_position = None

    if direction == 'left':
        new_position = (player_position[0], player_position[1] - 1)
    elif direction == 'right':
        new_position = (player_position[0], player_position[1] + 1)
    elif direction == 'top':
        new_position = (player_position[0] - 1, player_position[1])
    elif direction == 'bottom':
        new_position = (player_position[0] + 1, player_position[1])

    if 0 <= new_position[0] < 10 and 0 <= new_position[1] < 10:
        if data["map"][new_position[0]][new_position[1]] != 0:
            if data["map"][new_position[0]][new_position[1]] == 3:
                data["amount_food"] -= 1
            data["map"][player_position[0]][player_position[1]] = 1
            data["map"][new_position[0]][new_position[1]] = 2

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
    for row in map_data:
        for cell in row:
            if cell not in [0, 1, 2, 3]:
                return f"Invalid object '{cell}' found on map. Allowed objects are 0, 1, 2, 3."
    return None


def validate_player_function(context):
    if 'movePlayer' not in context:
        return "Function 'movePlayer' is not found in the code."
    elif not callable(context['movePlayer']):
        return "'movePlayer' is not a function."
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


def process_game_with_user_code(file_obj, map_data, max_moves):
    if not file_obj.name.endswith('.py'):
        return {"error": "Uploaded file is not a Python (.py) file."}, False

    file_path = os.path.join('', file_obj.name)
    with open(file_path, 'wb+') as destination:
        for chunk in file_obj.chunks():
            destination.write(chunk)

    syntax_error = validate_python_syntax(file_path)
    if syntax_error:
        return {"error": syntax_error}, False

    context = {}
    with open(file_path, 'r') as f:
        code = f.read()
    exec(code, context)

    function_error = validate_player_function(context)
    if function_error:
        return {"error": function_error}, False

    movePlayer = context['movePlayer']

    map_error = validate_map_objects(map_data)
    if map_error:
        return {"error": map_error}, False

    player_surrounded_error = validate_player_surrounded(map_data)
    if player_surrounded_error:
        return {"error": player_surrounded_error}, False

    fruits_accessibility_error = validate_fruits_accessibility(map_data)
    if fruits_accessibility_error:
        return {"error": fruits_accessibility_error}, False

    # Логика игры
    store = {}
    moves_log = []
    moves_count = 0
    game_result = "victory"
    infinite_loop_detected = False

    while moves_count < max_moves:
        limited_map = get_field_around_player(2, 2, map_data)
        direction, store = movePlayer(limited_map, store)

        direction_error = validate_move_direction(direction)
        if direction_error:
            return {"error": direction_error}, False

        moves_log.append({
            "move_number": moves_count + 1,
            "direction": direction,
            "store": store.copy()
        })
        moves_count += 1

        new_data = move(direction, {"map": map_data, "store": store, "player_moves": len(moves_log), "amount_food": 5})

        if new_data["amount_food"] == 0:
            game_result = "victory"
            break

        if len(moves_log) > 1 and moves_log[-1]["direction"] == moves_log[-2]["direction"]:
            infinite_loop_detected = True

    if infinite_loop_detected:
        game_result = "infinite_loop_detected"
    elif moves_count == max_moves:
        game_result = "max_moves_reached"

    return {
        "game_result": game_result,
        "moves": moves_log
    }, True
