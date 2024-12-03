import ulid
from rest_framework import serializers, fields
from rest_framework.exceptions import MethodNotAllowed, ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone
from core.fields import ULIDField as CoreULIDField
from core.utils import get_serialized_data, dynamic_exclude


class ULIDField(fields.Field):
    default_error_messages = {
        'invalid': _('"{value}" is not a valid ULID.'),
    }

    def to_internal_value(self, data):
        try:
            return ulid.parse(data)
        except (AttributeError, ValueError):
            self.fail('invalid', value=data)

    def to_representation(self, value):
        return str(ulid.parse(value))

# Mapping for CoreULIDField
serializers.ModelSerializer.serializer_field_mapping[CoreULIDField] = ULIDField


class BaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = None
        exclude = dynamic_exclude(model)
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
        }

    def get_nested_serializer_fields(self) -> dict:
        return {}

    def get_nested_serializer_fields_example(self) -> dict:
        return {
            'key': {
                'serializer': 'SerializerClass itself',
                'kwargs': {}
            }
        }

    def handle_nested_serializers(self, instance, data):
        nested_serializers = self.get_nested_serializer_fields()
        if nested_serializers is None:
            raise ImproperlyConfigured(_('Make sure to return the dict in get_nested_serializer_fields()'))
        try:
            for key, nested_serializer in nested_serializers.items():
                data[key] = get_serialized_data(nested_serializer['serializer'], getattr(instance, key, None), **nested_serializer['kwargs'])
        except KeyError as e:
            raise ImproperlyConfigured(_(f'Make sure that the nested serializer dict has {e} key'))
        except TypeError as e:
            raise ImproperlyConfigured(_(f'{e}, Make sure to follow the nested serializer format defined in get_nested_serializer_fields_example()'))

    def to_representation(self, instance):
        data = super().to_representation(instance)
        self.handle_nested_serializers(instance, data)
        return data

    def get_current_user(self):
        return (
            self.context.get('request').user
            if self.context.get('request') and self.context.get('request').user.is_authenticated
            else None
        )

    def get_datetime_now(self):
        return timezone.now()

    def set_from_context(self, validated_data):
        """Setting validated data from context"""
        pass

    def set_audit_fields(self, validated_data, audit_by_field, audit_at_field):
        extra_data = dict()
        if hasattr(self.Meta.model, audit_by_field):
            extra_data[audit_by_field] = self.get_current_user()
        if hasattr(self.Meta.model, audit_at_field):
            extra_data[audit_at_field] = self.get_datetime_now()
        for key, value in extra_data.items():
            validated_data[key] = value if key not in validated_data else validated_data[key]

    def create(self, validated_data):
        if self.Meta.model is None:
            raise NotImplementedError(_('BaseSerializer must be subclassed with a model'))
        self.set_from_context(validated_data)
        self.set_audit_fields(validated_data, 'created_by', 'created_at')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if self.Meta.model is None:
            raise NotImplementedError(_('BaseSerializer must be subclassed with a model'))
        self.set_audit_fields(validated_data, 'updated_by', 'updated_at')
        return super().update(instance, validated_data)


class BaseSubSerializer(BaseSerializer):

    class Meta:
        model = None
        exclude = dynamic_exclude(model)

    def prevent_actions(self):
        method = self.context.get('request').method
        raise MethodNotAllowed(method=method)

    def create(self, validated_data):
        self.prevent_actions()

    def update(self, instance, validated_data):
        self.prevent_actions()
