from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from django.apps import apps
from .serializers import FileUploadSerializer

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

    # Поиск позиции куда нужно пойти
    if direction == 'left':
        new_position = (player_position[0], player_position[1] - 1)
    elif direction == 'right':
        new_position = (player_position[0], player_position[1] + 1)
    elif direction == 'top':
        new_position = (player_position[0] - 1, player_position[1])
    elif direction == 'bottom':
        new_position = (player_position[0] + 1, player_position[1])

    if 0 <= new_position[0] < 10 and 0 <= new_position[1] < 10:
        # Проверяем, не стоит ли на новой позиции стена
        if data["map"][new_position[0]][new_position[1]] != 0:
            if data["map"][new_position[0]][new_position[1]] == 3:
                data["amount_food"] -= 1
            data["map"][player_position[0]][player_position[1]] = 1
            data["map"][new_position[0]][new_position[1]] = 2

    return data

class GameWithFileUploadView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file_obj = serializer.validated_data['file']
            file_path = os.path.join('', file_obj.name)

            with open(file_path, 'wb+') as destination:
                for chunk in file_obj.chunks():
                    destination.write(chunk)

            context = {}
            with open(file_path, 'r') as f:
                code = f.read()

            exec(code, context)

            if 'movePlayer' not in context:
                return Response({"error": "Функция 'movePlayer' не найдена в загруженном файле."},
                                status=status.HTTP_400_BAD_REQUEST)

            movePlayer = context['movePlayer']

            map_data = request.data.get("map", None)
            max_moves = request.data.get("max_moves", 500)  # По умолчанию 500 ходов

            if map_data is None or len(map_data) != 10 or any(len(row) != 10 for row in map_data):
                return Response({"error": "Invalid map format. Map must be a 10x10 grid."},
                                status=status.HTTP_400_BAD_REQUEST)

            store = {}
            moves_log = []
            moves_count = 0
            game_result = "victory"
            infinite_loop_detected = False

            while moves_count < max_moves:
                limited_map = get_field_around_player(2, 2, map_data)

                direction, store = movePlayer(limited_map, store)

                moves_log.append({
                    "move_number": moves_count + 1,
                    "direction": direction,
                    "store": store.copy()
                })
                moves_count += 1

                new_data = move(direction,
                                {"map": map_data, "store": store, "player_moves": len(moves_log), "amount_food": 5})

                if new_data["amount_food"] == 0:
                    game_result = "victory"
                    break

                if len(moves_log) > 1 and moves_log[-1]["direction"] == moves_log[-2]["direction"]:
                    infinite_loop_detected = True

            # Проверяем на зацикливание или превышение лимита ходов
            if infinite_loop_detected:
                game_result = "infinite_loop_detected"
            elif moves_count == max_moves:
                game_result = "max_moves_reached"

            # Возвращаем результат игры и лог ходов
            return Response({
                "game_result": game_result,
                "moves": moves_log
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
