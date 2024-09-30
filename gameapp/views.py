from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GameSerializer
from .game_logic import Game
import base64
import os

class GameAPIView(APIView):
    def post(self, request):
        # Сериализуем входные данные
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Получаем входные данные
                player1_code = base64.b64decode(serializer.validated_data['player1_code']).decode('utf-8')
                player2_code = base64.b64decode(serializer.validated_data['player2_code']).decode('utf-8')
                game_map = serializer.validated_data['game_map']
                max_moves = serializer.validated_data['max_moves']

                # Записываем коды игроков в файлы
                player1_file = self.save_player_code(player1_code, 'player1_code.py')
                player2_file = self.save_player_code(player2_code, 'player2_code.py')

                # Запускаем игру
                game = Game(player1_file, player2_file, game_map, max_moves)
                result = game.run()

                return Response(result, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def save_player_code(self, player_code, filename):
        """Сохраняет код игрока в файл."""
        file_path = os.path.join('/Users/Davlet/PycharmProjects/drf/alatoo/Snake_Game', filename)  # Укажите ваш путь
        with open(file_path, 'w') as file:
            file.write(player_code)
        return file_path
