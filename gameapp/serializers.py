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
                format, imgstr = data.split(';base64,')
                ext = format.split('/')[-1]
                data = base64.b64decode(imgstr)
                file = io.BytesIO(data)
                file.name = 'uploaded_file.' + ext
                return file
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
    file = Base64FileField()

    def validate_file(self, value):
        if not value.name.endswith('.py'):
            raise serializers.ValidationError("Файл должен быть с расширением .py")
        return value

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
    file = Base64FileField(
        required=True,
        help_text="Файл с кодом игрока для решения задачи. Должен быть .py."
    )
