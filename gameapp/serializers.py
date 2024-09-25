from rest_framework import serializers
import base64
from django.core.files.base import ContentFile

class Base64FileField(serializers.FileField):
    def to_internal_value(self, data):
        global decoded_file
        if isinstance(data, str):
            if 'data:' in data and ';base64,' in data:
                data = data.split(';base64,')[-1]
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_file')

            file_name = 'gameapp/file.py'
            return ContentFile(decoded_file, name=file_name)

        self.fail('invalid_data')

class FileUploadSerializer(serializers.Serializer):
    file = Base64FileField()

    def validate_file(self, value):
        if not value.name.endswith('.py'):
            raise serializers.ValidationError("Файл должен быть с расширением .py")
        return value
