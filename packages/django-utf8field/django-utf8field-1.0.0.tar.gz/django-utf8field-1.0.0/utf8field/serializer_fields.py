from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .validators import text_input_validator, file_input_validator


class UTF8TextSerializerField(serializers.CharField):
    def __init__(self, four_byte_detection=False, *args, **kwargs):
        self.four_byte_detection = four_byte_detection
        super(UTF8TextSerializerField, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        text_input_validator(data, self.four_byte_detection, ValidationError)
        return data


class UTF8CharSerializerField(serializers.CharField):
    def __init__(self, four_byte_detection=False, *args, **kwargs):
        self.four_byte_detection = four_byte_detection
        super(UTF8CharSerializerField, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        text_input_validator(data, self.four_byte_detection, ValidationError)
        return data


class UTF8FileSerializerField(serializers.FileField):
    def __init__(self, max_content_length=None, four_byte_detection=False, *args, **kwargs):
        self.max_content_length = max_content_length
        self.four_byte_detection = four_byte_detection
        super(UTF8FileSerializerField, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        file_input_validator(data, self.max_content_length, self.four_byte_detection, ValidationError)
        return data
