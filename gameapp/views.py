from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileUploadSerializer, GameSettingsSerializer
from .utils import process_game_with_user_code

class GameWithFileUploadView(APIView):
    serializer_class = GameSettingsSerializer

    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file_1_obj = serializer.validated_data['file_1']
            file_2_obj = serializer.validated_data['file_2']
            map_data = request.data.get("map")
            max_moves = int(request.data.get("max_moves"))

            game_result, success = process_game_with_user_code(file_1_obj,file_2_obj, map_data, max_moves)

            if success:
                return Response(game_result, status=status.HTTP_200_OK)
            else:
                return Response(game_result, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
