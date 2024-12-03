import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class StrongPasswordValidator:

    def validate(self, password, user=None):

        if not any(char.islower() for char in password) or not any(char.isupper() for char in password):
            raise ValidationError(
                _("Password must contain both uppercase and lowercase letters."),
                code='password_no_case_variation',
            )

        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _("Password must contain at least one digit."),
                code='password_no_number',
            )

        pattern = r'[!@#$%^&*()_+\-=\[\]{};\'\\:"|<>,./?]'
        if not re.search(pattern, password):
            raise ValidationError(
                _("Password must contain at least one special character (!@#$%^&*()_+-= etc.)."),
                code='password_no_special',
            )

    def get_help_text(self):
        return _(
            "Your password must contain both uppercase and lowercase letters, "
            "at least one number, and at least one special character (!@#$%^&*()_+-= etc.)."
        )
