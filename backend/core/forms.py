import ulid
from django import forms
from django.core import exceptions
from django.utils.translation import gettext as _


class ULIDField(forms.CharField):
    default_error_messages = {
        'invalid': _('Enter a valid ULID.'),
    }

    def prepare_value(self, value):
        if isinstance(value, ulid.ULID):
            return str(value)
        return value

    def to_python(self, value):
        value = super().to_python(value)
        if value in self.empty_values:
            return None
        try:
            value = ulid.parse(value)
        except (AttributeError, ValueError):
            raise exceptions.ValidationError(self.error_messages['invalid'], code='invalid')
        return value
