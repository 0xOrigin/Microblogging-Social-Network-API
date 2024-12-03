from smtplib import SMTPException
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from celery import shared_task
import mimetypes


@shared_task
def send_email(
        subject,
        message,
        html_content=None,
        from_email=f"{settings.EMAIL_HOST_NAME} <{settings.EMAIL_HOST_USER}>",
        to=None,
        cc=None,
        bcc=None,
        attachments=None,
        reply_to=None,
        headers=None,
    ):
    email = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=from_email,
        to=to,
        cc=cc,
        bcc=bcc,
        reply_to=reply_to,
        headers=headers,
    )
    
    if attachments:
        for attachment in attachments:
            with open(attachment, 'rb') as file:
                mime_type, _ = mimetypes.guess_type(attachment)
                email.attach(file.name, file.read(), mime_type or 'application/octet-stream')
                
    if html_content:
        email.attach_alternative(html_content, 'text/html')
    try:
        result = (
            email.send(fail_silently=False)
            if settings.IS_SEND_EMAIL_ENABLED 
            else 'Send email is disabled, check settings.IS_SEND_EMAIL_ENABLED to enable it'
        )
    except SMTPException as err:
        return f"{err}"
    return result


def send_bulk_email(datatuple, fail_silently=False):
    return EmailMultiAlternatives(datatuple).send(fail_silently=fail_silently)
