from __future__ import unicode_literals

import re

from django.utils.translation import ugettext_lazy as _

re_pattern = re.compile(u'[^\u0000-\u07FF\uE000-\uFFFF]', re.UNICODE)


def filter_using_re(unicode_string):
    return re_pattern.sub(u'\uFFFD', unicode_string)


def text_input_validator(data, four_byte_detection, ValidationError):
    if data:
        if '\x00' in data:
            raise ValidationError(
                _('NULL character detected'), code='null')

        if four_byte_detection and data != filter_using_re(data):
            raise ValidationError(
                _('4 Byte UTF8-characters detected'), code='4byte')


def file_input_validator(data, max_content_length, four_byte_detection, ValidationError):
    if data:
        try:
            content = data.read()
            decoded = content.decode('utf-8')

            if four_byte_detection and decoded != filter_using_re(decoded):
                raise ValidationError(
                    _('4 Byte UTF8-characters detected'), code='4byte')

            if max_content_length and len(content) > max_content_length:
                raise ValidationError(_(
                    'The content of the text file cannot be longer then %(max_content_length)s characters.' % {
                        'max_content_length': max_content_length}))

        except UnicodeError:
            raise ValidationError(_('Non UTF8-content detected'), code='utf8')
