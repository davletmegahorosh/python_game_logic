import random
from pprint import pprint

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
    if not isinstance(map_error, int):
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
    amount_food = map_error
    fruits_1 = 0
    fruits_2 = 0
    winner = None

    while moves_count < max_moves:

        limited_map_1 = get_field_around_player(3, 2, map_data)

        try:
            direction_1, store_1 = movePlayer_1(limited_map_1, store_1, 3)
        except Exception as e:
            return {
            'winner' : "player_2",
            'error' : f"Error while running movePlayer_1: {e}"}, False

        direction_error_1 = validate_move_direction(direction_1)
        if direction_error_1:
            return {'winner' : "player_2", "error": direction_error_1}, False

        limited_map_2 = get_field_around_player(4, 2, map_data)

        try:
            direction_2, store_2 = movePlayer_2(limited_map_2, store_2, 4)
        except Exception as e:
            return {
                'winner': "player_1",
                'error': f"Error while running movePlayer_1: {e}"}, False

        direction_error_2 = validate_move_direction(direction_2)

        if direction_error_2:
            return {'winner' : "player_1", "error": direction_error_2}, False

        moves_log.append({
            "move_number": moves_count + 1,
            "player_1": {"direction" : direction_1,
                         "store" : store_1.copy()},
            "player_2": {"direction": direction_2,
                         "store": store_2.copy()},
        })

        moves_count += 1

        new_data = move(direction_1, direction_2, {
            "map": map_data,
            "amount_food": amount_food,
            "player_moves": len(moves_log),
            "fruits_1" : fruits_1,
            "fruits_2" : fruits_2,
            "is_alive_1" : True,
            "is_alive_2" : True
        })

        if not new_data["is_alive_1"]:
            reason = new_data['reason']
            game_result = '1 player step on BOBMB' if reason == 'bomb' else '2 player steped on 1 player'
            return {
                "winner" : "player_2",
                "game_result": game_result,
                "moves": moves_log
            }, True

        if not new_data["is_alive_2"]:
            reason = new_data['reason']
            game_result = '2 player step on BOBMB' if reason == 'bomb' else '1 player steped on 2 player'
            return {
                "winner" : "player_1",
                "game_result": game_result,
                "moves": moves_log
            }, True

        amount_food = new_data['amount_food']
        fruits_1 = new_data['fruits_1']
        fruits_2 = new_data['fruits_2']

        if new_data["amount_food"] == 0:
            break

    if moves_count == max_moves:
        if fruits_1 > fruits_2:
            winner = "player_1"
            game_result = "max_moves_reached, player 1 collected more fruits"
        elif fruits_1 < fruits_2:
            winner = "player_2"
            game_result = "max_moves_reached, player 2 collected more fruits"
        else:
            winner = "mr Arthur"
            game_result = "max_moves_reached, draw, "


    return {
        "winner" : winner,
        "game_result": game_result,
        "moves": moves_log
    }, True
