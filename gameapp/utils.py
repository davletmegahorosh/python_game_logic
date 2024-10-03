import random
from .utils2 import *
def process_game_with_user_code(file_1_obj, file_2_obj, map_data, max_moves):
    random_result = random.randint(0,1)
    first_move = "First_player"
    if random_result:
        file_1_obj, file_2_obj = file_2_obj, file_1_obj
        first_move = "Second_Player"


    syntax_error_1 = validate_python_syntax(file_1_obj)
    if syntax_error_1:
        return {"error": syntax_error_1}, False

    context_1 = {}
    with open(file_1_obj,"r") as f:
        code_1 = f.read()
    exec (code_1, context_1)

    function_error_1 = validate_player_function(context_1, "player_1")
    if function_error_1:
        return {"error": function_error_1}, False

    movePlayer_1 = context_1['movePlayer']

    syntax_error_2 = validate_python_syntax(file_2_obj)
    if syntax_error_2:
        return {"error": syntax_error_2}, False

    context_2 = {}
    with open(file_2_obj,"r") as f:
        code_2 = f.read()
    exec (code_2, context_2)


    function_error_2 = validate_player_function(context_2, "player_2")
    if function_error_2:
        return {"error": function_error_2}, False

    movePlayer_2 = context_2['movePlayer']


    map_error = validate_map_objects(map_data)
    if map_error:
        return {"error": map_error}, False

    player_surrounded_error = validate_player_surrounded(map_data)
    if player_surrounded_error:
        return {"error": player_surrounded_error}, False

    fruits_accessibility_error = validate_fruits_accessibility(map_data)
    if fruits_accessibility_error:
        return {"error": fruits_accessibility_error}, False

    store_1 = {}
    store_2 = {}
    moves_log = []
    moves_count = 0
    game_result = "victory"


    while moves_count < max_moves:

        limited_map_1 = get_field_around_player(3, 2, map_data)
        # print(limited_map_1)
        for i in range(len(limited_map_1)):
            for j in range(len(limited_map_1[i])):
                if j == 3:
                    limited_map_1[i][j] = 2
                elif j == 2:
                    limited_map_1[i][j] = 3

        # try:
        direction_1, store_1 = movePlayer_1(limited_map_1, store_1)
        # except Exception as e:
        #     print(f"Error while running movePlayer: {e}")
        #     return (f"Error while running movePlayer_1: {e}"), False

        direction_error_1 = validate_move_direction(direction_1)
        if direction_error_1:
            return {"error": direction_error_1}, False

        limited_map_2 = get_field_around_player(4, 2, map_data)
        # print(limited_map_2)
        for i in range(len(limited_map_2)):
            for j in range(len(limited_map_2[i])):
                if j == 4:
                    limited_map_2[i][j] = 2
                elif j == 2:
                    limited_map_2[i][j] = 3

        # try:
        direction_2, store_2 = movePlayer_2(limited_map_2, store_2)
        # except Exception as e:
        #     print(f"Error while running movePlayer: {e}")
        #     return (f"Error while running movePlayer_2: {e}"), False

        direction_error_2 = validate_move_direction(direction_2)
        if direction_error_2:
            return {"error": direction_error_2}, False

        moves_log.append({
            "move_number": moves_count + 1,
            "player_1": {"direction" : direction_1,
                         "store" : store_1.copy()},
            "player_2": {"direction": direction_2,
                         "store": store_2.copy()},
        })

        moves_count += 1

        new_data = move(direction_1, direction_2, {"map": map_data, "amount_food": 5, "player_moves": len(moves_log)})
        # new_data = move(direction_2, {"map": map_data, "store": store_2, "player_moves": len(moves_log), "amount_food": 5},4)
        #
        # if new_data["amount_food"] == 0:
        #     game_result = "victory"
        #     break

    if moves_count == max_moves:
        game_result = "max_moves_reached"

    return {
        "game_result": game_result,
        "moves": moves_log
    }, True
