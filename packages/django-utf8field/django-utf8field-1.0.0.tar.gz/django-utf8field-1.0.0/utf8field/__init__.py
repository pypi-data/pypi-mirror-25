try:                        # pragma: no cover
    from rest_framework.serializers import ModelSerializer
    from utf8field.fields import UTF8TextField, UTF8CharField, UTF8FileField
    from utf8field.serializer_fields import UTF8TextSerializerField, UTF8CharSerializerField, UTF8FileSerializerField

    ModelSerializer.serializer_field_mapping[UTF8TextField] = UTF8TextSerializerField
    ModelSerializer.serializer_field_mapping[UTF8CharField] = UTF8CharSerializerField
    ModelSerializer.serializer_field_mapping[UTF8FileField] = UTF8FileSerializerField
except ImportError as e:    # pragma: no cover
    # We won't be needing the restframework anyway
    pass
