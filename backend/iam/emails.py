from django.template.loader import render_to_string
from core.emails import send_email
from django.utils.translation import gettext as _


def send_user_registration_email(instance):
    context = {
        'name': instance.name
    }
    html_content = render_to_string('iam/registration_email.html', context)
    return send_email.delay(
        subject=_('Registration Confirmation'),
        message=_('Registration Confirmation'),
        html_content=html_content,
        to=[instance.email,]
    )
