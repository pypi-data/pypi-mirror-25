from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from .validators import text_input_validator, file_input_validator


class UTF8CharField(models.CharField):
    description = _('A char field containing only UTF-8 text')

    def __init__(self, four_byte_detection=False, *args, **kwargs):
        self.four_byte_detection = four_byte_detection
        super(UTF8CharField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(UTF8CharField, self).deconstruct()

        if self.four_byte_detection:
            kwargs['four_byte_detection'] = self.four_byte_detection

        return name, path, args, kwargs

    def validate(self, data, model_instance):
        text_input_validator(data, self.four_byte_detection, ValidationError)
        return super(UTF8CharField, self).validate(data, model_instance)


class UTF8TextField(models.TextField):
    description = _('A text field containing only UTF-8 text')

    def __init__(self, four_byte_detection=False, *args, **kwargs):
        self.four_byte_detection = four_byte_detection
        super(UTF8TextField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(UTF8TextField, self).deconstruct()

        if self.four_byte_detection:
            kwargs['four_byte_detection'] = self.four_byte_detection

        return name, path, args, kwargs

    def validate(self, data, model_instance):
        text_input_validator(data, self.four_byte_detection, ValidationError)
        return super(UTF8TextField, self).validate(data, model_instance)


class UTF8FileField(models.FileField):
    description = _('A text file containing only UTF-8 text')

    def __init__(self, max_content_length=None, four_byte_detection=False, *args, **kwargs):
        self.max_content_length = max_content_length
        self.four_byte_detection = four_byte_detection
        super(UTF8FileField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(UTF8FileField, self).deconstruct()

        if self.max_content_length:
            kwargs['max_content_length'] = self.max_content_length

        if self.four_byte_detection:
            kwargs['four_byte_detection'] = self.four_byte_detection

        return name, path, args, kwargs

    def validate(self, data, model_instance):
        file_input_validator(data, self.max_content_length, self.four_byte_detection, ValidationError)
        return super(UTF8FileField, self).validate(data, model_instance)
