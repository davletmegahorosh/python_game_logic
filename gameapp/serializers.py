from rest_framework.exceptions import ValidationError
import base64
import io
from rest_framework import serializers


class Base64FileField(serializers.FileField):
    """
    Serializer field for handling base64 encoded files.
    """

    def to_internal_value(self, data):
        if isinstance(data, str):
            try:
                # Декодируем данные из base64
                decoded_data = base64.b64decode(data)

                output_file_path = f'{self.source}.py'  # Используем self.source для уникальности

                with open(output_file_path, 'wb') as output_file:
                    output_file.write(decoded_data)

                return output_file_path
            except (TypeError, ValueError, base64.binascii.Error) as e:
                raise ValidationError("Invalid base64 data")
        else:
            return super().to_internal_value(data)

    def to_representation(self, value):
        if value:
            file = io.BytesIO(value.read())
            return 'data:{0};base64,{1}'.format('application/octet-stream', base64.b64encode(file.getvalue()).decode())
        return ''

class FileUploadSerializer(serializers.Serializer):
    file_1 = Base64FileField()
    file_2 = Base64FileField()


class GameSettingsSerializer(serializers.Serializer):
    map = serializers.ListField(
        child=serializers.ListField(
            child=serializers.IntegerField(),
            min_length=10,
            max_length=10
        ),
        min_length=10,
        max_length=10
    )
    max_moves = serializers.IntegerField(
        min_value=1,
        required=True,
        help_text="Максимальное количество ходов в игре."
    )
    file_1 = Base64FileField(
        required=True,
        help_text="Файл с кодом игрока для решения задачи. Должен быть .py."
    )

    file_2 = Base64FileField(
        required=True,
        help_text="Файл с кодом игрока для решения задачи. Должен быть .py."
    )
