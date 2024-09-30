from rest_framework import serializers

class GameSerializer(serializers.Serializer):
    player1_code = serializers.CharField()
    player2_code = serializers.CharField()
    game_map = serializers.ListField(
        child=serializers.ListField(
            child=serializers.IntegerField(min_value=0, max_value=5),
            min_length=15, max_length=15
        ),
        min_length=15, max_length=15
    )
    max_moves = serializers.IntegerField(min_value=1)
