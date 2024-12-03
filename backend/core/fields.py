import ulid
from django.core import exceptions
from django.db import models
from django.utils.translation import gettext as _
from core import forms


def new_ulid():
    return ulid.new()


class ULIDField(models.Field):
    default_error_messages = {
        'invalid': _('“%(value)s” is not a valid ULID.'),
    }
    description = _('Universally Unique Lexicographically Sortable Identifier')
    empty_strings_allowed = False

    def __init__(self, verbose_name=None, **kwargs):
        kwargs.setdefault('max_length', 26)
        super().__init__(verbose_name, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs

    def get_internal_type(self):
        return 'UUIDField'

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return self.to_python(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return None
        if not isinstance(value, ulid.ULID):
            value = self.to_python(value)
        return value.uuid if connection.features.has_native_uuid_field else str(value)

    def from_db_value(self, value, expression, connection):
        return str(self.to_python(value)) if value is not None else None

    def to_python(self, value):
        if value is None:
            return None
        try:
            return ulid.parse(value)
        except (AttributeError, ValueError):
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value}
            )

    def formfield(self, **kwargs):
        return super().formfield(
            **{
                'form_class': forms.ULIDField,
                **kwargs,
            }
        )
