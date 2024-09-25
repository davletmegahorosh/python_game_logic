from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileUploadSerializer
from .utils import process_game_with_user_code

class GameWithFileUploadView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file_obj = serializer.validated_data['file']
            map_data = request.data.get("map", None)
            max_moves = request.data.get("max_moves", 500)

            game_result, success = process_game_with_user_code(file_obj, map_data, max_moves)

            if success:
                return Response(game_result, status=status.HTTP_200_OK)
            else:
                return Response(game_result, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
