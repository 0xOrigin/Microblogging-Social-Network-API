from django.dispatch import receiver
from django.db.models.signals import post_migrate
from django.conf import settings
from iam.apps import IamConfig
from iam.utils import create_superuser
from django.utils.translation import gettext as _


@receiver(post_migrate)
def perform_post_migrate_actions(sender, **kwargs):
    if not settings.ALLOW_POST_MIGRATE_SEEDERS:
        return
    if sender.name != IamConfig.name:
        return

    create_superuser()
