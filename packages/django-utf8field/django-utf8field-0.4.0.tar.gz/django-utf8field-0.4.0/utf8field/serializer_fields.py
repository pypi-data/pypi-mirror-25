from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .validators import text_input_validator, file_input_validator


class UTF8TextSerializerField(serializers.CharField):
    def to_internal_value(self, data):
        text_input_validator(data, ValidationError)
        return data


class UTF8CharSerializerField(serializers.CharField):
    def to_internal_value(self, data):
        text_input_validator(data, ValidationError)
        return data

class UTF8FileSerializerField(serializers.CharField):
    def __init__(self, max_content_length=None, *args, **kwargs):
        self.max_content_length = max_content_length
        super(UTF8FileSerializerField, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        file_input_validator(data, self.max_content_length, ValidationError)
        return data